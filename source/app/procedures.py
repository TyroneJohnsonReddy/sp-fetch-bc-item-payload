from __future__ import annotations
import requests
from snowflake.snowpark import Session
import sys
from snowflake_module_handler import SnowflakeHandler


def fetch_data(url, headers):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def fetch_all_data(base_url, headers):
    """Fetch all paginated data from the API."""
    data = fetch_data(base_url, headers)
    all_data = data["value"]  # Initialize with the first page of data

    # Fetch data in loop
    while "@odata.nextLink" in data:
        next_link = data["@odata.nextLink"]
        data = fetch_data(next_link, headers)
        all_data.extend(data["value"])  # Append only once per page

    return all_data


def get_bc_data(session: Session):
    msg = None
    try:
        print("fetching data from business central")
        # Get the _snowflake module (real or mock)
        snowflake_module = SnowflakeHandler.get_snowflake_module()
        credentials = snowflake_module.get_username_password("cred")

        # get a token for the request
        BC_TENANT_ID = "7acdd053-13fa-4b36-85d9-18131c8cda43"
        TOKEN_ENDPOINT = (
            f"https://login.microsoftonline.com/{BC_TENANT_ID}/oauth2/v2.0/token"
        )

        payload = {
            "grant_type": "client_credentials",
            "client_id": credentials.username,
            "client_secret": credentials.password,
            "scope": "https://api.businesscentral.dynamics.com/.default",
        }

        # Request token
        token_response = requests.post(TOKEN_ENDPOINT, data=payload)
        token = token_response.json().get("access_token")
        if token is None:
            raise Exception(
                f"Failed to get Business Central access token:{token_response.text}"
            )

        base_url = f"https://api.businesscentral.dynamics.com/v2.0/7acdd053-13fa-4b36-85d9-18131c8cda43/Production/ODataV4/Company('iKhoKha')/ItemPayloadStatus?$filter=Entry_Type eq 'Sale' and Status eq 'Success'"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        all_data = fetch_all_data(base_url, headers)
        print(len(all_data))

        snow_df = session.create_dataframe(all_data)
        snow_df.write.mode("overwrite").saveAsTable(
            "IKHOKHA_BI.STITCH_IKHOKHA.BC_ITEM_PAYLOAD"
        )
        msg = f"Wrote {snow_df.count()} rows to table IKHOKHA_BI.STITCH_IKHOKHA.BC_ITEM_PAYLOAD"
        return msg

    except Exception as ex:
        msg = f"Error occurred: {str(ex)}"
        print(msg)
        raise RuntimeError(msg)


# For local debugging
# Beware you may need to type-convert arguments if you add input parameters
if __name__ == "__main__":
    # Create a local Snowpark session
    with Session.builder.getOrCreate() as session:
        if len(sys.argv) > 1:
            print(get_bc_data(session, *sys.argv[1:]))
        else:
            print(get_bc_data(session))
            session.close()
