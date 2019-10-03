# hello-user

The Users API prototype

## Dependencies

* Redis (persistent storage)

## Local environment setup

```
docker-compose up --build -d
```

## First service check

```
curl -H "Content-Type: application/json" -XPUT localhost:5000/hello/johndoe -d '{"dateOfBirth": "1970-01-01"}'

curl localhost:5000/hello/johndoe
```

## Tests run

```
docker-compose exec api pytest
```

## Diagrams

You can find [AWS](./diagrams/aws.jpg) and [GCP](./diagrams/gcp.jpg) diagrams in `diagrams/`

## Additional achievements

* CI/CD pipeline (Instructions in `Jenkinsfile` and `Jenkinsfile.deploy` included)
* Jenkins Kubernetes plugin pod temlate (Spec in `pipeline/`)
* Helm chart (The whole one is in `helm/`)

## TODO

* Add the Terraform state for EKS cluster and Elasticache infrastructure
* Try out Redis-cluster setup for scalability profits
