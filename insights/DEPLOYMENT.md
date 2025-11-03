# Deployment Guide

## Local Development Setup

### Prerequisites

- Python 3.8+
- pip or conda
- Git (optional)

### Installation Steps

1. **Navigate to insights folder:**

```bash
cd insights
```

2. **Create virtual environment:**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Configure Azure credentials:**

```bash
# Copy template
cp .env.example .env

# Edit .env with your credentials
# (or provide them via Streamlit UI)
```

5. **Run the application:**

```bash
streamlit run app.py
```

6. **Access the dashboard:**
   Open browser to `http://localhost:8501`

---

## Docker Deployment

### Single Container

1. **Build the image:**

```bash
docker build -t insights-dashboard:latest .
```

2. **Create .env file:**

```bash
cp .env.example .env
# Edit with your credentials
```

3. **Run the container:**

```bash
docker run -d \
  -p 8501:8501 \
  --env-file .env \
  --name insights-dashboard \
  insights-dashboard:latest
```

4. **Access the dashboard:**
   `http://localhost:8501`

5. **View logs:**

```bash
docker logs -f insights-dashboard
```

6. **Stop the container:**

```bash
docker stop insights-dashboard
docker rm insights-dashboard
```

### Docker Compose

1. **Setup:**

```bash
cp .env.example .env
# Edit .env with your credentials
```

2. **Deploy:**

```bash
docker-compose up -d
```

3. **View logs:**

```bash
docker-compose logs -f
```

4. **Stop:**

```bash
docker-compose down
```

---

## Production Deployment Options

### Option 1: Azure Container Instances (ACI)

1. **Push image to Azure Container Registry:**

```bash
# Login to ACR
az acr login --name myregistry

# Tag image
docker tag insights-dashboard:latest myregistry.azurecr.io/insights-dashboard:latest

# Push
docker push myregistry.azurecr.io/insights-dashboard:latest
```

2. **Deploy to ACI:**

```bash
az container create \
  --resource-group myResourceGroup \
  --name insights-dashboard \
  --image myregistry.azurecr.io/insights-dashboard:latest \
  --ports 8501 \
  --environment-variables-from-file env.list \
  --restart-policy Always
```

### Option 2: Azure App Service

1. **Create deployment:**

```bash
# Using Azure CLI
az webapp create \
  --resource-group myResourceGroup \
  --plan myAppServicePlan \
  --name insights-dashboard \
  --runtime "python|3.11"
```

2. **Configure app settings:**

```bash
az webapp config appsettings set \
  --resource-group myResourceGroup \
  --name insights-dashboard \
  --settings \
    AZURE_APP_ID="your_value" \
    AZURE_CLIENT_ID="your_value" \
    AZURE_CLIENT_SECRET="your_value" \
    AZURE_TENANT_ID="your_value"
```

3. **Deploy code:**

```bash
az webapp deployment source config-zip \
  --resource-group myResourceGroup \
  --name insights-dashboard \
  --src deployment.zip
```

### Option 3: Kubernetes

1. **Create Docker image:**

```bash
docker build -t insights-dashboard:latest .
docker push myregistry.azurecr.io/insights-dashboard:latest
```

2. **Create Kubernetes deployment.yaml:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: insights-dashboard
spec:
  replicas: 1
  selector:
    matchLabels:
      app: insights-dashboard
  template:
    metadata:
      labels:
        app: insights-dashboard
    spec:
      containers:
        - name: insights-dashboard
          image: myregistry.azurecr.io/insights-dashboard:latest
          ports:
            - containerPort: 8501
          env:
            - name: AZURE_APP_ID
              valueFrom:
                secretKeyRef:
                  name: azure-secrets
                  key: app-id
            - name: AZURE_CLIENT_ID
              valueFrom:
                secretKeyRef:
                  name: azure-secrets
                  key: client-id
            - name: AZURE_CLIENT_SECRET
              valueFrom:
                secretKeyRef:
                  name: azure-secrets
                  key: client-secret
            - name: AZURE_TENANT_ID
              valueFrom:
                secretKeyRef:
                  name: azure-secrets
                  key: tenant-id
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /_stcore/health
              port: 8501
            initialDelaySeconds: 60
            periodSeconds: 30
---
apiVersion: v1
kind: Service
metadata:
  name: insights-dashboard
spec:
  selector:
    app: insights-dashboard
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8501
  type: LoadBalancer
```

3. **Deploy:**

```bash
# Create secret
kubectl create secret generic azure-secrets \
  --from-literal=app-id='your_value' \
  --from-literal=client-id='your_value' \
  --from-literal=client-secret='your_value' \
  --from-literal=tenant-id='your_value'

# Deploy
kubectl apply -f deployment.yaml

# Check status
kubectl get pods
kubectl logs <pod-name>
```

### Option 4: GitHub Actions (CI/CD)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy Insights Dashboard

on:
  push:
    branches: [main]
    paths:
      - "insights/**"

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Build Docker image
        run: |
          docker build -t insights-dashboard:${{ github.sha }} .
          docker tag insights-dashboard:${{ github.sha }} insights-dashboard:latest

      - name: Login to Registry
        uses: docker/login-action@v1
        with:
          registry: myregistry.azurecr.io
          username: ${{ secrets.REGISTRY_USERNAME }}
          password: ${{ secrets.REGISTRY_PASSWORD }}

      - name: Push to registry
        run: |
          docker push myregistry.azurecr.io/insights-dashboard:${{ github.sha }}
          docker push myregistry.azurecr.io/insights-dashboard:latest

      - name: Deploy to ACI
        uses: azure/container-instances-deploy-action@v1
        with:
          action: "create"
          resource-group: ${{ secrets.AZURE_RESOURCE_GROUP }}
          name: insights-dashboard
          image: myregistry.azurecr.io/insights-dashboard:latest
          ports: 8501
          environment-variables: |
            AZURE_APP_ID=${{ secrets.AZURE_APP_ID }}
            AZURE_CLIENT_ID=${{ secrets.AZURE_CLIENT_ID }}
            AZURE_CLIENT_SECRET=${{ secrets.AZURE_CLIENT_SECRET }}
            AZURE_TENANT_ID=${{ secrets.AZURE_TENANT_ID }}
```

---

## Scaling & Performance Optimization

### For High Traffic

1. **Increase Python workers:**

```bash
streamlit run app.py \
  --logger.level=warning \
  --client.showErrorDetails=false
```

2. **Use caching:**
   Add to `app.py`:

```python
@st.cache_data(ttl=300)
def get_dashboard_data(time_range):
    # expensive operation
    pass
```

3. **Load balancing:**
   Deploy multiple replicas behind a load balancer

### For Large Data Sets

1. Adjust `REFRESH_INTERVAL` in `config.py` to reduce API calls
2. Add time range restrictions for queries
3. Use query pagination for large result sets
4. Consider sampling data for very large datasets

---

## Monitoring & Logging

### Application Insights Monitoring

Monitor the dashboard itself with Application Insights:

```python
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.tracer import Tracer

exporter = AzureExporter(connection_string='YOUR_CONNECTION_STRING')
tracer = Tracer(exporter=exporter)

with tracer.span(name='fetch_data'):
    # your code
    pass
```

### Container Logging

1. **Docker:**

```bash
docker logs insights-dashboard
```

2. **Docker Compose:**

```bash
docker-compose logs -f
```

3. **Kubernetes:**

```bash
kubectl logs -f <pod-name>
```

---

## Backup & Disaster Recovery

1. **Backup configuration:**

```bash
# Backup .env and any custom configs
tar -czf insights-backup-$(date +%Y%m%d).tar.gz .env config.py
```

2. **Versioning:**
   Tag Docker images with version numbers

```bash
docker tag insights-dashboard:latest insights-dashboard:v1.0.0
```

---

## Troubleshooting Deployment

| Issue                      | Solution                                               |
| -------------------------- | ------------------------------------------------------ |
| Port already in use        | Change port: `streamlit run app.py --server.port 8502` |
| Permission denied (Docker) | Run with `docker-compose` or check file permissions    |
| Connection timeout         | Verify Azure credentials and network access            |
| High memory usage          | Reduce refresh interval or number of charts            |
| Slow response              | Add caching or increase time between refreshes         |

---

## Security Best Practices

1. **Credentials:**

   - Never commit `.env` to version control
   - Use Azure Key Vault for production secrets
   - Rotate client secrets regularly

2. **Network:**

   - Use VPN for accessing sensitive dashboards
   - Implement IP whitelisting
   - Use SSL/TLS for connections

3. **Access Control:**

   - Implement authentication layer (ngrok, OAuth2, etc.)
   - Audit dashboard access
   - Limit data exposure

4. **Container Security:**
   - Scan images for vulnerabilities
   - Use minimal base images
   - Run containers as non-root

---

## Maintenance

### Regular Tasks

- **Weekly:** Review logs for errors
- **Monthly:** Update dependencies (`pip list --outdated`)
- **Quarterly:** Review and optimize queries
- **Annually:** Security audit and penetration testing

### Update Process

1. Test updates in development first
2. Update `requirements.txt`
3. Rebuild Docker image
4. Deploy to staging
5. Verify functionality
6. Deploy to production

---

## Support & Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Azure Monitor Documentation](https://docs.microsoft.com/en-us/azure/azure-monitor/)
- [KQL Query Language](https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
