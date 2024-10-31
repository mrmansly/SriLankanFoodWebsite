path "auth/approle/role/sld-role/secret-id" {
  capabilities = ["create", "update"]
}
path "auth/approle/role/sld-role/role-id" {
  capabilities = ["read"]
}
