### How to run the restaurant recommendation model

#### Docker build
1. Before running the docker build, ensure that you are in root directory of the project ('Restaurant_Recommendation' folder): 
```
docker build --tag <docker_image_name> .
```
The above command will create the docker image

### Run locally
2. Run the docker image that we created in previous step:
```
docker run --name <container_name> -p 5000:5000 <docker_image_name>
```
Ensure that port is accurate.

3. After running the above command, you should see this in command prompt: "Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)"

4. Then you can go to browser and enter the url along with hashed_email: 
eg: http://localhost:5000/recommend?hashed_email=9003b3e5e7cafba48612b3f4ac936bf5

Ensure that port is accurate along with localhost in above mentioned url

5. You should see a list of 3 recommended restaurants for each hashed_email:  
eg: results: ['focrestaurant32hsa07a-4', '13gastrowine1603gas', 'blukouzina82fps33a-4']