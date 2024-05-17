import os

import aws_cdk as cdk

from codepipeline.pipelinecdk import pipeline

app = cdk.App()
pipeline(app, "codepipeline",
  
    )

app.synth()