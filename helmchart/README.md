datapusher-plus
==========
CKAN Datapusher Plus helm chart

Current chart version is `1.0.0`


## TODOS
- [ ] add new datapusher plus values to chart values table in README.md
- [ ] add option to retreive secrets using aws secrets driver
- [ ] init db in datapusher-init/datapusher-init.py instead of using docker entrypoint
- [ ] wait for db connection using datapusher-init/datapusher-init.py

## Chart Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| datapusher.chunkSize | string | `"16384"` | Size of chunks of the data that is being downloaded in bytes |
| datapusher.datapusherRewriteResources | string | `"True"` | Enable or disable (boolean) whether datapusher should rewrite resources uploaded to CKAN's filestore, since datapusher takes the CKAN Site URL value for generating the resource URL. Default: False |
| datapusher.datapusherRewriteUrl | string | `"http://ckan"` |  |
| datapusher.datapusherSslVerify | string | `"0"` | Enable or disable (boolean) verification of SSL when trying to get resources. Default: True |
| datapusher.downloadTimeout | string | `"30"` | Timeout limit of the download request |
| datapusher.insertRows | string | `"250"` | Number of rows to take from the data and upload them as chunks to datastore |
| datapusher.maxContentLength | string | `"10485760"` | Maximum size of content to be uploaded in bytes. |
| fullnameOverride | string | `""` |  |
| image.pullPolicy | string | `"IfNotPresent"` |  |
| image.repository | string | `"tnristwdb/datapusher-plus"` |  |
| image.tag | string | `"latest"` |  |
| imagePullSecrets | list | `[]` |  |
| ingress.annotations | object | `{}` |  |
| ingress.enabled | bool | `false` |  |
| ingress.hosts[0].host | string | `"chart-example.local"` |  |
| ingress.hosts[0].paths | list | `[]` |  |
| ingress.tls | list | `[]` |  |
| nameOverride | string | `""` |  |
| nodeSelector | object | `{}` |  |
| podSecurityContext | object | `{}` |  |
| replicaCount | int | `1` |  |
| resources | object | `{}` |  |
| securityContext | object | `{}` |  |
| service.port | int | `8800` |  |
| service.type | string | `"ClusterIP"` |  |
| serviceAccount.annotations | object | `{}` |  |
| serviceAccount.create | bool | `true` |  |
| serviceAccount.name | string | `nil` |  |
| tolerations | list | `[]` |  |
