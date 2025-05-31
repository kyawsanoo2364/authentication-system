"""This script generates a .env file for setup"""

if __name__ in "__main__":
    data = """#This is from mailtrap integration smtp
EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=true
EMAIL_USE_SSL=false
#other
DEBUG=true
FRONTEND_URL=
FROM_EMAIL= #your email address for send to user
GOOGLE_CLIENT_ID= #google cloud api -> oauth_client_id
SOCIAL_PASSWORD=DJFIJjadfqei2d4f7e1a #As you like
#After building react file
VITE_BACKEND_API_URL=http://127.0.0.1:8000/api/v1
VITE_GOOGLE_CLIENT_ID="""

    with open(".env.local", "w") as f:
        f.write(data)
        print("Generated .env file")
