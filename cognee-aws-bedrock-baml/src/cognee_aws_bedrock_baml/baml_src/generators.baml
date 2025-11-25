// BAML Generator Configuration for cognee-aws-bedrock-baml

generator py_client {
  output_type python/pydantic
  output_dir "../baml_client"
  version "0.214.0"
  default_client_mode sync
}
