# Local Minikube deployment

This is a copy of your existing project: Express frontend, Flask backend and MongoDB. The assignment specifies Flask frontend and Express backend, so this existing architecture needs instructor acceptance or a separate application refactor before submission.

Status: deployed and verified from the terminal output supplied in this chat. The `student-local` node reached Ready; frontend, backend and MongoDB each reached `1/1 Running` in the `student-app` namespace. Form submissions were verified in the MongoDB `student_database.students` collection. Screenshots are held by the student and should be included with this package.

## Submission contents and audit notes

- `frontend/Dockerfile` and `backend/Dockerfile`: image build instructions.
- `k8s/apps.yaml`: namespace, three Deployments, three Services and MongoDB PVC.
- All containers have CPU/memory requests and limits. All Deployments have readiness probes; MongoDB's exec probe allows 10 seconds.
- MongoDB storage uses a 1 Gi PVC and survives pod replacement. Frontend is a NodePort; Flask and MongoDB are internal ClusterIP Services.
- No database password or cloud credential is included. This local exercise uses MongoDB without authentication inside the cluster; a Kubernetes Secret is not used. ClusterIP does not provide authentication. For shared or production environments, add MongoDB authentication, inject credentials through Secrets, restrict network access, and use HTTPS.
- Current manifests have readiness probes, but no liveness or startup probes. The backend `/api` probe checks the Flask process, not database connectivity. These are documented limitations rather than claims of production readiness.
- Add the three screenshots to a `screenshots/` directory before submission. Keep passwords, `.env`, private keys and generated dependency folders out of Git.

Suggested Git layout is this folder's existing structure. From this directory, inspect `git status` before adding files to your assignment repository; commit the Dockerfiles, application files, `k8s/`, README and screenshots.

Start Docker Desktop using Linux containers. Install Minikube using https://minikube.sigs.k8s.io/docs/start/ if needed. In a terminal in this folder run each command in order; stop if a command fails:

```sh
minikube start --driver=docker -p student-local
minikube -p student-local image build -t student-backend:v1 ./backend
minikube -p student-local image build -t student-frontend:v1 ./frontend
kubectl --context=student-local apply -f k8s/apps.yaml
kubectl --context=student-local -n student-app rollout status deployment/mongodb --timeout=180s
kubectl --context=student-local -n student-app rollout status deployment/backend --timeout=180s
kubectl --context=student-local -n student-app rollout status deployment/frontend --timeout=180s
kubectl --context=student-local -n student-app get pods,services,pvc
kubectl --context=student-local -n student-app port-forward service/frontend 3000:3000
```

Keep port forwarding running, open http://localhost:3000 and submit a student. In another terminal verify that the submitted student is stored:

```sh
kubectl --context=student-local -n student-app exec deployment/mongodb -- mongosh student_database --quiet --eval 'db.students.find({}, {_id:0}).toArray()'
```

The browser calls Express, Express sends form data to the internal Flask Service, and Flask writes to the internal MongoDB Service. The NodePort Service can also be accessed using `minikube -p student-local service frontend -n student-app --url` (keep that terminal open on Windows).

Fixes in this copy: frontend starts directly with Node; submission uses the form encoding Flask expects; database errors return HTTP 503 instead of a false success. Existing repository files were not changed. MongoDB is for this local exercise and its PVC retains data between pod restarts.

For troubleshooting:

```sh
kubectl --context=student-local -n student-app get events --sort-by=.lastTimestamp
kubectl --context=student-local -n student-app logs deployment/backend
kubectl --context=student-local -n student-app logs deployment/frontend
```
