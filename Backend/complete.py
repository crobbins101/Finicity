import subprocess

# Specify the full path to the scripts
script_path = "C:\\Users\\crobb\\OneDrive\\Finicity\\Backend\\"

# Call auth.py
try:
    auth_process = subprocess.run(["python", script_path + "auth.py"], capture_output=True, text=True)
    print("Response from auth.py:")
    print(auth_process.stdout)
    if auth_process.returncode != 0:
        print("Error calling auth.py:", auth_process.stderr)
except subprocess.CalledProcessError as e:
    print("Error calling auth.py:", e.stderr)

# Call customer.py
try:
    customer_process = subprocess.run(["python", script_path + "customer.py"], capture_output=True, text=True)
    print("Response from customer.py:")
    print(customer_process.stdout)
    if customer_process.returncode != 0:
        print("Error calling customer.py:", customer_process.stderr)
except subprocess.CalledProcessError as e:
    print("Error calling customer.py:", e.stderr)

# Call consumer.py
try:
    consumer_process = subprocess.run(["python", script_path + "consumer.py"], capture_output=True, text=True)
    print("Response from consumer.py:")
    print(consumer_process.stdout)
    if consumer_process.returncode != 0:
        print("Error calling consumer.py:", consumer_process.stderr)
except subprocess.CalledProcessError as e:
    print("Error calling consumer.py:", e.stderr)

# Call connect.py
try:
    connect_process = subprocess.run(["python", script_path + "connect.py"], capture_output=True, text=True)
    print("Response from connect.py:")
    print(connect_process.stdout)
    if connect_process.returncode != 0:
        print("Error calling connect.py:", connect_process.stderr)
except subprocess.CalledProcessError as e:
    print("Error calling connect.py:", e.stderr)
