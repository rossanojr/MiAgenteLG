### Configurar repositorio local para git
<!--  -->
```bash
git config --local user.name "Juan Rossano"
git config --local user.email "juanrossano@gmail.com"
```

# Vaciar cualquier helper previo (opcional, pero buena práctica si quieres aislarlo)
```bash
git config --local credential.helper ""
```

# Usar el manejador de credenciales de Windows (permite login web)
```bash
git config --local credential.helper manager
```

# Aislar la credencial guardada a la ruta específica de este repositorio
```bash
git config --local credential.useHttpPath true
```

