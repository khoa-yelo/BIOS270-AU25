<<<<<<< HEAD
What micromamba command can you use to list all created environemnts?
micromamba env list

What micromamba command can you use to list all packages installed in a specific environment?
micromamba activate bioinfo_example
micromamba list

What micromamba command can you use to remove a package?
micromamba remove package_name

What micromamba command can you use to install a package from a specific channel?
micromamba install -c channel_name package_name

What micromamba command can you use to remove an environment?
micromamba env remove -n environment_name

What are all the r-base and Bioconductor packages that were installed in the bioinfo_example environment? (Hint: You may want to use one of the commands from your answers to the above questions, and combine it with the grep command.)
=======
# Write up 2: Environment Setup

## Part A: Micromambra 
*What is Micromamba*
It is a way to create environments locally, that way you don't have to install the libraries everytime you need to do something. It is tun locally 
A .yaml file is a file that has all the packages to be install, like the bioinfo_example.yaml that we used for the homework

To remember: --from history flag ensures that only explicitly installed packages are saved, keeping the environment file clean and minimal.
**Differences from the 2 yaml files?**
The latest .yaml file is the same as the first version but the latest has the rpy2 package and it also has the prefix: "/scratch/users/isagolda/envs/micromamba/envs/bioinfo_example"

**Questions to answer**
What micromamba command can you use to list all created environemnts?
````bash
micromamba env list
````
What micromamba command can you use to list all packages installed in a specific environment?
````bash
micromamba list -n name_of_environment
````
What micromamba command can you use to remove a package?
````bash
micromamba remove package_name
````

What micromamba command can you use to install a package from a specific channel?
````bash
micromamba install -c channel_name package_name
````
What micromamba command can you use to remove an environment?
````bash
micromamba env remove -n environment_name
````
What are all the r-base and Bioconductor packages that were installed in the bioinfo_example environment? (Hint: You may want to use one of the commands from your answers to the above questions, and combine it with the grep command.)
**Bioconductor Packages (18 total):**
- bioconductor-apeglm
- bioconductor-biobase
- bioconductor-biocgenerics
- bioconductor-biocparallel
- bioconductor-data-packages
- bioconductor-delayedarray
- bioconductor-deseq2
- bioconductor-genomeinfodb
- bioconductor-genomeinfodbdata
- bioconductor-genomicranges
- bioconductor-iranges
- bioconductor-matrixgenerics
- bioconductor-s4arrays
- bioconductor-s4vectors
- bioconductor-sparsearray
- bioconductor-summarizedexperiment
- bioconductor-xvector
- bioconductor-zlibbioc

**R Packages (200+ total):**
- r-abind
- r-ashr
- r-base
- r-ggplot2
- r-dplyr
- r-tidyverse
- r-shiny
- r-knitr
- r-rmarkdown
- ... (and 190+ more)

![python_example_plot](../Environment/scripts/python_example_plot.png)
![R_example_plot](../Environment/scripts/r_example_plot.png)
## Part B: Containers
Summary of what happened: 
1. Set of the Docker Hub and Stanford Gitlab connection
For me, I always had to use Apptainer instead of singularity 
2. Build Docker image
````bash
docker build -t bioinfo_exaple docker
docker build = build an image 
-t bioinfo_example = tag (name) it “bioinfo_example”
. = use the Dockerfile in the current directory
````

Then to tag them: 
Into Docker Hub:
````bash
docker tag bioinfo_example isagolda/bioinfo_example
````
- Creates a new tag (name) for the same image
- Format: `username/image-name`
- This tells Docker Hub where to store it

docker push isagolda/bioinfo_example
- Uploads the image to Docker Hub

Tag for Stanford GilLab:
````bash
docker tag bioinfo_example scr.svc.stanford.edu/<SUNetID>/containers/bioinfo_example
````
- Creates another tag for Stanford's registry
- Format: `registry-url/sunetid/containers/image-name`
I had to create a token from Stanford gitLab to login and then the bioinfo_example was uploaded successfully into container registry

3. Pull image to Farmshare with Singularity
Workflow: 
a. 
````bash
module load apptainer
apptainer remote login -u isagolda docker://scr.svc.stanford.edu
cd $SCRATCH
apptainer exec -B $SCRATCH:/data containers/bioinfo_example_latest.sif python /data/hello.py
````
**Why is the -B flag important?**
Without the -B flag, the Python script cannot be executed because containers are isolated environments that do not have access to the host filesystem by default. The container cannot see the hello.py file located in $SCRATCH.

4. Writing your own Dockerfile
````bash
# Use your existing image as the base
FROM bioinfo_example:latest

# Switch to root user to install system packages
USER root

# Install parasail via pip
RUN pip install parasail

# Install wget and foldseek from GitHub binary
RUN apt-get update && apt-get install -y wget && \
    wget https://github.com/steineggerlab/foldseek/releases/download/9-427df8a/foldseek-linux-avx2.tar.gz && \
    tar xvzf foldseek-linux-avx2.tar.gz && \
    mv foldseek/bin/foldseek /usr/local/bin/ && \
    rm -rf foldseek foldseek-linux-avx2.tar.gz && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch back to non-root user
USER $MAMBA_USER

# Set working directory
WORKDIR /workspace

docker build --platform linux/amd64 -f Dockerfile.v2 -t bioinfo_example:v2 .

docker tag bioinfo_example:v2 isagolda/bioinfo_example:v2

docker tag bioinfo_example:v2 scr.svc.stanford.edu/isagolda/containers/bioinfo_example:v2

docker push isagolda/bioinfo_example:v2

docker push scr.svc.stanford.edu/isagolda/containers/bioinfo_example:v2
````
And then you follow: 
1. Build
2. Tag
3. Push

![Docker_summit](../Duckerhub.png)




>>>>>>> 1ba1c28194b2094fa3627630931599cdb8aadb94
