sudo apt-get install openjdk-6-jre-headless
curl -O http://dist.neo4j.org/neo4j-community-1.9.2-unix.tar.gz
tar -xf neo4j-community-*.tar.gz
rm neo4j-community-*.tar.gz
neo4j-community-1.9.2/bin/neo4j start