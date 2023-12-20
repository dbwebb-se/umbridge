# Links
# azurerm docs https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/resource_group
# azure cli https://docs.microsoft.com/en-us/cli/azure/authenticate-azure-cli#sign-in-with-credentials-on-the-command-line
# structure https://thomasthornton.cloud/2021/06/07/getting-started-with-terraform-on-azure/
# followed https://docs.microsoft.com/en-us/azure/developer/terraform/create-linux-virtual-machine-with-infrastructure

# Configure the Azure provider

provider "azurerm" {
  features {}
}


# Get manual resource group
data "azurerm_resource_group" "manualUmbridge" {
  name = var.manual_resource_group_name

}

# Create a resource group if it doesn't exist
resource "azurerm_resource_group" "umbridge" {
  name     = var.terraform_resource_group_name
  location = var.location
}

# Create virtual network
resource "azurerm_virtual_network" "umbridgeNetwork" {
  name                = "umbridgeVnet"
  address_space       = ["10.0.0.0/16"]
  location            = var.location
  resource_group_name = azurerm_resource_group.umbridge.name
}

# Create subnet
resource "azurerm_subnet" "umbridgeSubnet" {
  name                 = "umbridgeSubnet"
  resource_group_name  = azurerm_resource_group.umbridge.name
  virtual_network_name = azurerm_virtual_network.umbridgeNetwork.name
  address_prefixes     = ["10.0.1.0/24"]
}

# Create public IPs
resource "azurerm_public_ip" "umbridgeIp" {
  name                = "umbrideIP"
  location            = var.location
  resource_group_name = azurerm_resource_group.umbridge.name
  allocation_method   = "Static"
  ip_version          = "IPv4"
}

# Create dns zone
data "azurerm_dns_zone" "umbridgeDNS" {
  name                = var.dns_name
  resource_group_name = data.azurerm_resource_group.manualUmbridge.name
}

# Create A record
resource "azurerm_dns_a_record" "dnsARecord" {
  count = length(var.dns_records)

  name                = var.dns_records[count.index]
  zone_name           = data.azurerm_dns_zone.umbridgeDNS.name
  resource_group_name = data.azurerm_resource_group.manualUmbridge.name
  ttl                 = var.record_ttl
  target_resource_id  = azurerm_public_ip.umbridgeIp.id
}

# Create Network Security Group and rule
resource "azurerm_network_security_group" "umbridgeSnG" {
  name                = "umbridgeSnG"
  location            = var.location
  resource_group_name = azurerm_resource_group.umbridge.name

  security_rule {
    name                       = "SSH"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
  security_rule {
    name                       = "HTTP"
    priority                   = 1002
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
  security_rule {
    name                       = "HTTPS"
    priority                   = 1003
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

# Create network interface
resource "azurerm_network_interface" "umbridgeNic" {
  name                = "umbridgeNic"
  location            = var.location
  resource_group_name = azurerm_resource_group.umbridge.name

  ip_configuration {
    name                          = "umbridgeNicConf"
    subnet_id                     = azurerm_subnet.umbridgeSubnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.umbridgeIp.id
  }
}

# Connect the security group to the network interface
resource "azurerm_network_interface_security_group_association" "example" {
  network_interface_id      = azurerm_network_interface.umbridgeNic.id
  network_security_group_id = azurerm_network_security_group.umbridgeSnG.id
}

data "azurerm_ssh_public_key" "umbridgeKey" {
  name                = var.ssh_name
  resource_group_name = data.azurerm_resource_group.manualUmbridge.name
}


# Create virtual machine
resource "azurerm_linux_virtual_machine" "umbridgeVM" {
  name                  = "umbridgeVM"
  location              = var.location
  resource_group_name   = azurerm_resource_group.umbridge.name
  network_interface_ids = [azurerm_network_interface.umbridgeNic.id]
  size                  = "Standard_B4ms"

  os_disk {
    name                 = "umbridgeDisk"
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Debian"
    offer     = "debian-10"
    sku       = "10"
    version   = "latest"
  }

  computer_name                   = "umbridge"
  admin_username                  = var.user_name
  disable_password_authentication = true

  admin_ssh_key {
    username   = var.user_name
    public_key = data.azurerm_ssh_public_key.umbridgeKey.public_key
    # public_key     = file("~/.ssh/umbridge.pem")
  }

  tags = {
    name = "server"
  }
}
