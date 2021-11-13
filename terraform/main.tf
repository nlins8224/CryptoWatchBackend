provider "google" {
 project = var.project
  region = var.region
}

module "cloud_function" {
 source = "modules\/cloud_functions"
 project = var.project
 function_name = "cloud_function"
 function_entry_point = "hello"
}