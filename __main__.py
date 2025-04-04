import pulumi
import pulumi_aws as aws
import pulumi_synced_folder as synced_folder

# Import the program's configuration settings.
config = pulumi.Config()
path = config.get("path") or "./www"


# Create an AWS resource (S3 Bucket)
bucket = aws.s3.BucketV2(
    'Static-Website-Bucket'
)

# Configure the bucket to host a static website.
bucket_website = aws.s3.BucketWebsiteConfigurationV2(
    'Static-Website-Bucket-Configuration',
    bucket=bucket.id,
    index_document={'suffix': 'index.html'},
    error_document={'key': 'error.html'},
)

# Create an IAM policy for the bucket
bucket_policy_resource = aws.s3.BucketPolicy(
    "bucketPolicyResource",
    bucket=bucket.id,  # Reference the bucket's ID
    policy=bucket.arn.apply(lambda arn : f"""{{
        "Version": "2012-10-17",
        "Statement": [
            {{
                "Effect": "Allow",
                "Principal": {{
                    "Service": "cloudfront.amazonaws.com"
                }},
                "Action": "s3:GetObject",
                "Resource": "{arn}/*"
            }}
        ]
    }}"""
))

ownership_controls = aws.s3.BucketOwnershipControls(
    "ownership-controls",
    bucket=bucket.bucket,
    rule={
        "object_ownership": "ObjectWriter",
    },
)

# Configure public ACL block on the new bucket
public_access_block = aws.s3.BucketPublicAccessBlock(
    "public-access-block",
    bucket=bucket.bucket,
    block_public_acls=False,
)

# Use a synced folder to manage the files of the website.
bucket_folder = synced_folder.S3BucketFolder(
    "bucket-folder",
    acl="public-read",
    bucket_name=bucket.bucket,
    path=path,
    opts=pulumi.ResourceOptions(depends_on=[ownership_controls, public_access_block]),
)

# Create a CloudFront CDN to distribute and cache the website.
cdn = aws.cloudfront.Distribution(
    "cdn",
    enabled=True,
    origins=[
        {
            "origin_id": bucket.arn,
            "domain_name": bucket_website.website_endpoint,
            "custom_origin_config": {
                "origin_protocol_policy": "http-only",
                "http_port": 80,
                "https_port": 443,
                "origin_ssl_protocols": ["TLSv1.2"],
            },
        }
    ],
    default_cache_behavior={
        "target_origin_id": bucket.arn,
        "viewer_protocol_policy": "redirect-to-https",
        "allowed_methods": [
            "GET",
            "HEAD"
        ],
        "cached_methods": [
            "GET",
            "HEAD"
        ],
        "default_ttl": 86400,
        "max_ttl": 31536000,
        "min_ttl": 60,
        "forwarded_values": {
            "query_string": False,
            "cookies": {
                "forward": "none",
            },
        },
    },
    custom_error_responses=[
        {
            "error_code": 404,
            "response_code": 404,
            "response_page_path": "/error.html",
        }
    ],
    restrictions={
        "geo_restriction": {
            "restriction_type": "none",
        },
    },
    viewer_certificate={
        "cloudfront_default_certificate": True,
    },
)


# Export the url of the bucket and the website URL.
pulumi.export('websiteURL', bucket_website.website_endpoint)
pulumi.export("cdnURL", pulumi.Output.concat("https://", cdn.domain_name))
