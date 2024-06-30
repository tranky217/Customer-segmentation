# Please accept the terms of the Snowplow Limited Use License Agreement to proceed. (https://docs.snowplow.io/limited-use-license-1.0/)
accept_limited_use_license = true

# Will be prefixed to all resource names
# Use this to easily identify the resources created and provide entropy for subsequent environments
prefix = "sp"

# The project to deploy the infrastructure into
project_id = "my-project-4195-423806"

# Where to deploy the infrastructure
region = "asia-southeast1"

# Update to the network you would like to deploy into
#
# Note: If you opt to use your own network then you will need to define a subnetwork to deploy into as well
network    = "default"
subnetwork = ""

# Update this to your IP Address
ssh_ip_allowlist = ["113.190.252.57/32"]
# Generate a new SSH key locally with `ssh-keygen`
# ssh-keygen -t rsa -b 4096 
ssh_key_pairs = [
  {
    user_name  = "snowplow"
    public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC2zQVbc8gW8xtabUO3X8ujGE74K6xjarixbAadNLVXyc2rsd4XpAf7Qaf5DyJGWVEaGPCrt/akjIFCh1avhZAF3NwMSDywGKtD6y0Zd9cuY6pVUf1+NvwZVL2WAtg1iN4QVW54HXKpFvmPSY75PLHScbzLJqCZ2fAq/eMRcTwk/Ygnq71J3KIcMxOjsZRpDey6DVJMS9ojm7IYjOYhZEmiCWYUtMdw0qHLf38E2Ry3OQ+ssqg1CTDx/4Llb8nfBCIcZ/DtTx/3tv0AW45Ao2wdr5+DHtRq7B813pfIswKg9aZQzdWd+4vZd5/KIY7gOiXsVHEhTrQcASMy5hrKg8b4PDuSSxmc/lZULW/VdyRtOHLiI3CwxPiJWOSJ5JrLITMdsdxRkuFxKBm7HTl5XJ+lusNdIVmUnXItELVf1dBXLM0Mt8OEjYMTtukTJEGh8Kcx9tP16DaFHP12jjdSX78Iq3KL3U214PTawCYTe7uicArojV4kSj5f16hNfqGhSpXtRYcg1VU1GJCYxrST7FvrX89HMbZbXejzED1j0RlMXEYNKEoTsdomj//vK5aEvStXkmEOJhGuzTc7NYwsUZfTWUurUzLqDComu/DRIB6VAqRN0Egzk/+c2499IyvoFbSW5Er9hxc1pHEqB8l9Nzr0mDFEhByiojkfr29axVFZBQ== tranky@LAPTOP-LPPE6FBE"
  }
]

# Iglu Server DNS output from the Iglu Server stack
iglu_server_dns_name = "http://34.49.134.181"
# Used for API actions on the Iglu Server
# Change this to the same UUID from when you created the Iglu Server
iglu_super_api_key = "4ea47389-9e4f-420a-801a-80edc236c8fe"

# Collector SSL Configuration (optional)
ssl_information = {
  certificate_id = ""
  enabled        = false
}

# --- TARGETS CONFIGURATION ZONE --- #

# --- Target: PostgreSQL
postgres_db_enabled = true

postgres_db_name     = "snowplow"
postgres_db_username = "snowplow"
# Change and keep this secret!
postgres_db_password = "2107"
# IP ranges that you want to query the Pipeline Postgres Cloud SQL instance from directly over the internet.  An alternative access method is to leverage
# the Cloud SQL Proxy service which creates an IAM authenticated tunnel to the instance
#
# Details: https://cloud.google.com/sql/docs/postgres/sql-proxy
#
# Note: this exposes your data to the internet - take care to ensure your allowlist is strict enough
postgres_db_authorized_networks = [
  {
    name  = "foo"
    value = "113.190.252.57/32"
  },
  {
    name  = "bar"
    value = "113.190.252.57/32"
  }
]
# Note: the size of the database instance determines the number of concurrent connections - each Postgres Loader instance creates 10 open connections so having
# a sufficiently powerful database tier is important to not running out of connection slots
postgres_db_tier = "db-g1-small"

# --- Target: BigQuery
bigquery_db_enabled = false

# To use an existing bucket set this to false
bigquery_loader_dead_letter_bucket_deploy = true
# Must be globally unique so will need to be updated before applying
bigquery_loader_dead_letter_bucket_name = "sp-bq-loader-dead-letter"

# --- ADVANCED CONFIGURATION ZONE --- #

# See for more information: https://registry.terraform.io/modules/snowplow-devops/collector-pubsub-ce/google/latest#telemetry
# Telemetry principles: https://docs.snowplowanalytics.com/docs/open-source-quick-start/what-is-the-quick-start-for-open-source/telemetry-principles/
user_provided_id  = ""
telemetry_enabled = false

# --- Extra Labels to append to created resources (optional)
labels = {}
