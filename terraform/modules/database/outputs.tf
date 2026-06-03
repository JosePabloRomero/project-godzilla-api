output "instance_name" {
  description = "Nombre de la instancia Cloud SQL"
  value       = google_sql_database_instance.postgres.name
}

output "private_ip_address" {
  description = "IP privada de la instancia Cloud SQL"
  value       = google_sql_database_instance.postgres.private_ip_address
}

output "database_name" {
  description = "Nombre de la base de datos"
  value       = google_sql_database.app_db.name
}

output "database_user" {
  description = "Usuario de base de datos"
  value       = google_sql_user.app_user.name
}

output "database_password" {
  description = "Contrasena de base de datos generada aleatoriamente"
  value       = random_password.db_password.result
  sensitive   = true
}
