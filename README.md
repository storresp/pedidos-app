# Sistema de Gestión de Pedidos - Pedido App 

Este repositorio contiene el sistema completo de **Gestión de Pedidos**, estructurado con una arquitectura moderna de microservicios, desplegado en Kubernetes utilizando **Helm** para el empaquetado y **ArgoCD** para GitOps.

## Cómo instalar el Chart manualmente con Helm

Si deseas realizar un despliegue manual sin depender de ArgoCD, puedes usar los siguientes comandos desde la raíz del proyecto:

1. **Instalar/Actualizar el Chart:**
   ```bash
   helm upgrade --install pedido-app ./charts/pedido-app -n dev --create-namespace
   ```

2. **Verificar el despliegue:**
   ```bash
   kubectl get all -n dev
   ```

3. **Desinstalar el Chart:**
   ```bash
   helm uninstall pedido-app -n dev
   ```

## Configuración de ArgoCD para Sincronización

El flujo de **GitOps** se gestiona mediante ArgoCD. La aplicación está configurada para sincronizarse automáticamente con la rama `juandi` de este repositorio.

- **Archivo de Configuración:** `environments/dev/application.yaml`
- **Namespace de destino:** `dev`
- **Políticas de Sincronización:**
  - `Automated Sync`: Sincronización automática al detectar cambios en Git.
  - `Prune`: Elimina recursos que ya no existen en Git.
  - `SelfHeal`: Corrige automáticamente cualquier drift manual en el clúster.

Para desplegar la aplicación de ArgoCD manualmente:
```bash
kubectl apply -f environments/dev/application.yaml
```

## Endpoints de Acceso

La aplicación utiliza un **Ingress Controller** para exponer los servicios. El host configurado es `pedido-app.local`.

###  Rutas (Paths):

| Servicio | Path | Descripción | Puerto Interno |
| :--- | :--- | :--- | :--- |
| **Frontend** | `/` | Interfaz de usuario (Vue.js) | 80 |
| **Backend** | `/pedidos/api/` | API Rest (Django) | 8000 |

### Configuración de Hosts:
Para acceder localmente, añade esta línea a tu archivo `hosts` (`/etc/hosts` en Linux/Mac o `C:\Windows\System32\drivers\etc\hosts` en Windows):
```text
127.0.0.1 pedido-app.local
```

---

## Auto-escalado (HPA)

El **Backend** cuenta con un **Horizontal Pod Autoscaler (HPA)** configurado para garantizar la disponibilidad:
- **Mínimo de réplicas:** 2
- **Máximo de réplicas:** 5
- **Métrica:** 80% de utilización de CPU.

