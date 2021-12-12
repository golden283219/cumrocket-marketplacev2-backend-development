variable "name" {
  type    = string
  default = "marketplace-worker"
}

variable "region" {
  type    = string
  default = "eu-west-2"
}

variable "instance_type" {
  type    = string
  default = "t2.micro"
}

variable "release_version" {
  type    = string
  default = "HEAD"
}

locals {
  timestamp = regex_replace(timestamp(), "[- TZ:]", "")
  backend_path = "/home/ubuntu/marketplacev2-backend"
}

packer {
  required_plugins {
    amazon = {
      version = ">= 0.0.1"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

source "amazon-ebs" "backend" {
  ami_name      = "${var.name}-${var.release_version}-${local.timestamp}"
  region        = var.region
  instance_type = var.instance_type
  source_ami_filter {
    filters = {
      name                = "ubuntu/images/*ubuntu-focal-20.04-*-server-*"
      architecture        = "x86_64"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    owners      = ["099720109477"]
  }
  ssh_username = "ubuntu"
  tags = {
    version = var.release_version
  }
}

build {
  sources = [
    "source.amazon-ebs.backend"
  ]

  provisioner "shell-local" {
    inline = [
      "cd ${path.root}/.. && git archive --format=tar ${var.release_version} | gzip > /tmp/marketplacev2-backend.tgz",
    ]
  }

  provisioner "file" {
    generated   = true
    source      = "/tmp/marketplacev2-backend.tgz"
    destination = "/tmp/"
  }

  provisioner "shell" {
    max_retries = 5
    environment_vars = [
      # "ENV=production",
    ]
    inline = [
      # Update & upgrade the system
      "sudo apt-get update",
      "DEBIAN_FRONTEND=noninteractive sudo apt-get upgrade -y",

      # Install packages
      "sudo apt-get install -y curl aptitude",
      "sudo aptitude install -y docker.io",
      "sudo systemctl enable --now docker",

      # Install SSM agent
      "sudo snap install amazon-ssm-agent --classic",

      # Install docker-compose
      "sudo curl -L \"https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose",
      "sudo chmod +x /usr/local/bin/docker-compose",

      # Install backend
      "mkdir -p ${local.backend_path}",
      "cd ${local.backend_path}",
      "tar xzfv /tmp/marketplacev2-backend.tgz",
      "touch .env",

      # Build Dockers
      "cd ${local.backend_path}",
      "sudo docker-compose -f docker-compose.workers.yml pull",
      "sudo docker-compose -f docker-compose.workers.yml build",

      # Run on reboot
      "(sudo crontab -l 2> /dev/null ; echo '@reboot (sleep 30s ; cd ${local.backend_path} ; /usr/local/bin/docker-compose -f docker-compose.workers.yml up -d )&' ) | sudo crontab -",
    ]
  }
}
