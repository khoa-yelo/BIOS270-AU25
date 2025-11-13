# Base image: includes Micromamba (a fast, minimal Conda) preinstalled
FROM mambaorg/micromamba:jammy

USER root

# Build-time variables: URL for an example FASTA and the name of the Conda environment
ARG RANDOM_FASTA=https://raw.githubusercontent.com/biopython/biopython/master/Doc/examples/ls_orchid.fasta
ARG MAMBA_ENV_NAME=bioinfo_example

# Install minimal OS dependencies needed for downloads and installers; then clean apt metadata to keep the image small
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates tar unzip vim nano\
    && rm -rf /var/lib/apt/lists/* 

# Install rclone
RUN curl -fsSL https://rclone.org/install.sh | bash 

# Install code-server (VS Code in the browser)
RUN curl -fsSL https://code-server.dev/install.sh | bash

USER $MAMBA_USER

# Set the working directory inside the container
WORKDIR /workspace

# Copy the environment YAML and example scripts into the container
COPY --chown=$MAMBA_USER:$MAMBA_USER . /workspace/

# Fetch an example FASTA into the workspace
RUN echo "Downloading example FASTA from: $RANDOM_FASTA"; \
    curl -fsSL "$RANDOM_FASTA" -o /workspace/example.fasta

# Create the Conda environment from YAML, then remove package caches to shrink the final image
RUN micromamba create -y -n "${MAMBA_ENV_NAME}" -f /workspace/bioinfo_example.yaml && \
    # Install the new package we want to add (this is an example, in practice you would want all your packages in the YAML file)
    micromamba install -n bioinfo_example -c conda-forge -c bioconda -c defaults -y rpy2 && \
    micromamba clean -a -y

# Make the new environment the default at runtime and ensure its binaries are first on PATH
ENV MAMBA_DEFAULT_ENV=${MAMBA_ENV_NAME}
ENV PATH=/opt/conda/envs/${MAMBA_ENV_NAME}/bin:$PATH


# Run example scripts to test the environment
RUN python /workspace/scripts/python_example.py && \
    python /workspace/scripts/rpy2_example.py && \
    Rscript /workspace/scripts/r_example.R \
    && echo "All example scripts ran successfully!"

# Default action when the container starts: open an interactive Bash shell
CMD ["/bin/bash"]