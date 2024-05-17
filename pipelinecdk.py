from aws_cdk import (
    Stack,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codecommit as codecommit,
    aws_codebuild as codebuild,
    aws_iam as iam
)
from constructs import Construct

class pipeline(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        projectRepository = codecommit.Repository(self, "javaProject",
                                     repository_name="java-project")  
        
       
        cfnRepository = projectRepository.node.default_child


        cfnRepository.add_property_override('Code', {
            'S3': {
                'Bucket': 'seis665-public',  
                'Key': 'java-project.zip',    
            },
            'BranchName': 'pipeline',
        })

       
        sourceArtifact = codepipeline.Artifact()
        commitSourceAction = codepipeline_actions.CodeCommitSourceAction(
            action_name="CodeCommit",
            repository=projectRepository,
            branch="pipeline",
            output=sourceArtifact
        )

       
        codeBuildProject = codebuild.PipelineProject(self, "BuildProject", 
                                                   environment=codebuild.BuildEnvironment(
                                                      compute_type=codebuild.ComputeType.SMALL, 
                                                      build_image=codebuild.LinuxBuildImage.STANDARD_5_0  
                                                  ) )

       
        buildPipelineAction = codepipeline_actions.CodeBuildAction(
            action_name="CodeBuild",
            project=codeBuildProject,
            input=sourceArtifact
        )

      
        deploymentPipeline = codepipeline.Pipeline(self, "MyPipeline",
                                         stages=[
                                             codepipeline.StageProps(
                                                 stage_name="Source",
                                                 actions=[commitSourceAction]
                                             ),
                                             codepipeline.StageProps(
                                                 stage_name="Build",
                                                 actions=[buildPipelineAction]
                                             )
                                         ])

        projectRepository.grant_read(deploymentPipeline.role)
        codeBuildProject.role.add_to_policy(
            iam.PolicyStatement(
                actions=["sts:AssumeRole"],
                resources=["*"]
            )
        )
