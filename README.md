## Git Clone

```sh
git clone --recurse-submodules https://github.com/NguyenPhamCode4You/ai-home-lab-docker-compose.git
```

## Complete restart

```sh
sudo docker stop $(sudo docker ps -a -q) && sudo docker rm $(sudo docker ps -a -q) && sudo docker rmi $(sudo docker images -a -q) && sudo docker volume rm $(sudo docker volume ls -q) && sudo docker network rm $(sudo docker network ls -q)
```

## Handling Ollama models

1. Create a Model file using example:

```Modelfile
from "./unsloth.Q8_0.gguf"
PARAMETER stop "<|im_start|>"
PARAMETER stop "<|im_end|>"
TEMPLATE """
<|im_start|>system
{{ .System }}<|im_end|>
<|im_start|>user
{{ .Prompt }}<|im_end|>
<|im_start|>assistant
"""
```

2. Copy Modelfile + gguf file into ollama docker container

```sh
docker cp ./unsloth.Q8_0.gguf ollama:/home
docker cp ./Modelfile ollama:/home
```

3. Exec into ollama container

```sh
docker exec -it ollama bash
```

4. Cd into /home and upload key to ollama if not yet

```sh
cat ~/.ollama/id_ed25519.pub
cat /usr/share/ollama/.ollama/id_ed25519.pub

cd /home
```

5. ollama Create model from file + push

```sh
ollama create nichealpham/lora-8b -f Modelfile
ollama push nichealpham/lora-8b
```
