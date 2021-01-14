ipfs_node_address='192.168.137.62'
mkdir -p /tmp/ipfs-docker-staging
mkdir -p /tmp/ipfs-docker-data
docker run -d --name ipfs-node -v /tmp/ipfs-docker-staging:/export -v /tmp/ipfs-docker-data:/data/ipfs -p 8080:8080 -p 4001:4001 -p ${ipfs_node_address}:5001:5001 ipfs/go-ipfs:latest

docker exec -it ipfs-node sh << EOF
ipfs config --json API.HTTPHeaders.Access-Control-Allow-Origin '["http://${ipfs_node_address}:5001", "http://localhost:3000", "http://127.0.0.1:5001", "https://webui.ipfs.io"]'
ipfs config --json API.HTTPHeaders.Access-Control-Allow-Methods '["PUT", "POST"]'
EOF
docker stop ipfs-node
docker start ipfs-node

#Alternatywnie:
docker run -d --name ipfs-node -p 8080:8080 -p 4001:4001 -p 5001:5001 ipfs/go-ipfs:latest
http://127.0.0.1:5001/webui  #webui
