from dotenv import load_dotenv
import boto3
import os
from jinja2 import Template


# Load environment variables
load_dotenv()

# AWS Configuration
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

def s3_client():
    return boto3.client('s3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )

def double_render(text):
    # print("Testing"*100)
    # filename = 'documents/qHiJSwc1L6A3bRfgbrmfRokeTo71lP.pdf'
    if 'documents' in text:
        filename = text
    else:
        return text

    s3 = s3_client()
    try:
        # Generate temporary URL (expires in 2 minutes)
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': os.getenv('S3_BUCKET_NAME'), 'Key': filename},
            ExpiresIn=8400
        )
        # return redirect(url)
        return url
    except Exception as e:
        return str(e), 404

def refresh_s3_link(html_template):
    template = Template(html_template)
    result = template.render(get_s3url=double_render)
    return result


if __name__ == '__main__':
    test = """
                    {{double_render}} >>
                      <p class="card-text large-text-e">
                            decided.<br>
                            The new committee assum decision-making while disclaiming accountability for past violations by the former management, prioritizing adherence to the law and society bylaws
                            {{get_s3url('documents/uvJ93NHyMyuw9nyjzJqbtWovP5n2tb.pdf')}}
                        </p>
                        <p class="card-text">
                            <a href="{{get_s3url('documents/uvJ93NHyMyuw9nyjzJqbtWovP5n2tb.pdf')}}">Download Reference Document</a>
                        </p>
    """
    rendered_text = refresh_s3_link(test)
    print(rendered_text)
    # template = Template(test)
    # result = template.render(get_s3url=double_render)
    # print(result)