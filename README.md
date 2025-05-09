(WIP) will add more details

Manifests
* flask-app1
* flask-app2
* proxysql
* mysql
* prometheus
* grafana

Topology
* app: flask-app1 -> flask-app2 -> proxysql -> mysql
* monitoring
    * flask-app1 exporter -> promoetheus -> grafana
    * flask-app2 exporter -> promoetheus -> grafana
    * proxyql exporter -> promoetheus -> grafana

Deployment
* kubectl apply -f xxx.yaml
* create proxysql user (one time)

```
CREATE USER 'proxyuser'@'%' IDENTIFIED WITH mysql_native_password BY 'proxyuser_password';
GRANT ALL PRIVILEGES ON *.* TO 'proxyuser'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

* create blogdb (one time)
```
CREATE DATABASE blogdb IF NOT EXISTS;
```

Test data preparation
* run locust at manifest level, and run post_blog task. In my testing I ran >10,000 requests and created that many blog records in DB.

Reproduce
1. hit endpoint: 127.0.0.1:8081/get_all_blogs to run the long polling query (fetch all DB records)
2. hit endpoint: 127.0.0.1:8081/health, should be working as pod is not down and this endpoint is not dependent on DB resources
3. hit endpoint: 127.0.0.1:8081/get_blog/1, should fail as proxysql connections are running out and blocked, expect retries
