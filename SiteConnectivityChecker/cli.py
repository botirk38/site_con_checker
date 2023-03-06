import argparse
def read_user_cli_args():
    parser = argparse.ArgumentParser(prog="ConChecker",description='Check if a website is online')
    parser.add_argument("-u","--urls",metavar="URLs",nargs="+",type=str,default=[],help="enter one or more urls to check")
    parser.add_argument(
        "-f",
        "--input-file",
        metavar="FILE",
        type=str,
        default="",
        help="read URLs from a file",)

    parser.add_argument(
    "-a",
    "--asynchronous",
    action="store_true",
    help="check websites asynchronously")
    
    return parser.parse_args()
    
def display_result(result,url,error=""):
    if result:
        print(f"{url} is online")
    else:
        print(f"{url} is offline")
        if error:
            print(f"Error: {error}")
