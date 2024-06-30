# Please accept the terms of the Snowplow Limited Use License Agreement to proceed. (https://docs.snowplow.io/limited-use-license-1.0/)
accept_limited_use_license = true

# Will be prefixed to all resource names
# Use this to easily identify the resources created and provide entropy for subsequent environments
prefix = "sp"

# The project to deploy the infrastructure into
project_id = "my-project-4195-423806"

# Where to deploy the infrastructure
region = "asia-southeast1"

# --- Default Network
# Update to the network you would like to deploy into
#
# Note: If you opt to use your own network then you will need to define a subnetwork to deploy into as well
network    = "default"
subnetwork = ""

# --- SSH
# Update this to your IP Address
ssh_ip_allowlist = ["42.119.180.50/32"]
# Generate a new SSH key locally with `ssh-keygen`
# ssh-keygen -t rsa -b 4096 
ssh_key_pairs = [
  {
    user_name  = "snowplow"
    public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC2zQVbc8gW8xtabUO3X8ujGE74K6xjarixbAadNLVXyc2rsd4XpAf7Qaf5DyJGWVEaGPCrt/akjIFCh1avhZAF3NwMSDywGKtD6y0Zd9cuY6pVUf1+NvwZVL2WAtg1iN4QVW54HXKpFvmPSY75PLHScbzLJqCZ2fAq/eMRcTwk/Ygnq71J3KIcMxOjsZRpDey6DVJMS9ojm7IYjOYhZEmiCWYUtMdw0qHLf38E2Ry3OQ+ssqg1CTDx/4Llb8nfBCIcZ/DtTx/3tv0AW45Ao2wdr5+DHtRq7B813pfIswKg9aZQzdWd+4vZd5/KIY7gOiXsVHEhTrQcASMy5hrKg8b4PDuSSxmc/lZULW/VdyRtOHLiI3CwxPiJWOSJ5JrLITMdsdxRkuFxKBm7HTl5XJ+lusNdIVmUnXItELVf1dBXLM0Mt8OEjYMTtukTJEGh8Kcx9tP16DaFHP12jjdSX78Iq3KL3U214PTawCYTe7uicArojV4kSj5f16hNfqGhSpXtRYcg1VU1GJCYxrST7FvrX89HMbZbXejzED1j0RlMXEYNKEoTsdomj//vK5aEvStXkmEOJhGuzTc7NYwsUZfTWUurUzLqDComu/DRIB6VAqRN0Egzk/+c2499IyvoFbSW5Er9hxc1pHEqB8l9Nzr0mDFEhByiojkfr29axVFZBQ== tranky@LAPTOP-LPPE6FBE"
  }
]

# --- Snowplow Iglu Server
iglu_db_name     = "iglu"
iglu_db_username = "iglu"
# Change and keep this secret!
iglu_db_password = "2107"

# Used for API actions on the Iglu Server
# Change this to a new UUID and keep it secret!
iglu_super_api_key = "4ea47389-9e4f-420a-801a-80edc236c8fe"

# NOTE: To push schemas to your Iglu Server, you can use igluctl
# igluctl: https://docs.snowplowanalytics.com/docs/pipeline-components-and-applications/iglu/igluctl
# igluctl static push --public schemas/ http://CHANGE-TO-MY-IGLU-IP 00000000-0000-0000-0000-000000000000

# See for more information: https://github.com/snowplow-devops/terraform-google-iglu-server-ce#telemetry
# Telemetry principles: https://docs.snowplowanalytics.com/docs/open-source-quick-start/what-is-the-quick-start-for-open-source/telemetry-principles/
user_provided_id  = ""
telemetry_enabled = false

# --- SSL Configuration (optional)
ssl_information = {
  certificate_id = ""
  enabled        = false
}

# --- Extra Labels to append to created resources (optional)
labels = {}
