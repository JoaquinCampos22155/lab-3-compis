provider "digitalocean" {
  token = var.digitalocean_token
}

resource "digitalocean_droplet" "web" {
  image  = "ubuntu-24-10-x64"
  name   = "example-droplet"
  region = "nyc1"
  size   = "s-1vcpu-512mb-10gb"
}
