# DNS Blacklist Attack Simulation

## Overview:
This project demonstrates how **DNS blacklisting** can be used to identify malicious or suspicious IP addresses. The script compares a list of IP addresses to known blacklisted IPs and outputs whether each IP is blacklisted or not.

### Objective:
The primary objective of this project is to simulate a **DNS blacklist attack**. The Python script (`dns_blacklist.py`) checks the IPs in the provided directory against a blacklist of known malicious IPs, simulating the detection of harmful traffic using DNS filtering.

---

## Technologies Used:
- **Python**: Programming language used for creating the script.
- **DNS Blacklist**: Concept of blocking or flagging IPs/domains as malicious.
- **Terminal/Command Line**: Used to run the script and view outputs.

## How to Download and Set Up the DNS Blacklist Repository:

1. **Clone the DNS Blacklist Repository**:
    - I used a Python-based DNS blacklist script available at [Bitbucket - EthanR/dns-blacklist](https://bitbucket.org/ethanr/dns-blacklists) to simulate the blacklist attack.
    - To download the DNS blacklist repository, follow these steps:
      - Open your terminal and clone the repository:
        ```bash
        git clone https://bitbucket.org/ethanr/dns-blacklists.git
        ```
      - Navigate to the directory containing the cloned repository:
        ```bash
        cd dns-blacklists
        ```

2. **Setting Up the Blacklist**:
    - Once inside the `dns-blacklists` folder, I extracted the contents and removed any **unnecessary files** that were not relevant to my project.
    - Then, I created a new folder called `suspect_IP` inside the `bad_lists/` directory, where I stored the **list of IPs** I wanted to check against the blacklists.
    - Specifically, I used the **`IP_Blacklist.txt`** file to populate the blacklisted IP addresses.

3. **Customize the List**:
    - I opened the `IP_Blacklist.txt` file and manually copied the first few IP addresses (for example, the first 5), and then I deleted the rest of the IPs for testing purposes.
    - I placed the edited list of blacklisted IPs inside the `suspect_IP` folder, ready to be checked by the Python script.

---

## How to Run:
### Prerequisites:
- Python 3.x installed on your machine.
- Basic understanding of using the command line/terminal.

### Steps:
1. **Clone the Repository**:
    To get the project files, clone the repository:
    ```bash
    git clone https://github.com/yourusername/DNS-Blacklist-Attack-Simulation.git
    ```

2. **Navigate to the Project Directory**:
    Change into the project directory:
    ```bash
    cd DNS-Blacklist-Attack-Simulation
    ```

3. **Run the Script**:
    Run the following command to execute the Python script:
    ```bash
    python dns_blacklist.py bad_lists/suspect_IP
    ```
    This command will:
    - Take the **IP addresses** from the `suspect_IP` folder.
    - Compare each IP against the **blacklisted IPs** found in the `bad_lists` folder.
    - Output whether each IP is blacklisted or not.

---

## Example Output:
After running the script, the output in the terminal will show whether each IP from the `suspect_IP` list is blacklisted:

```bash
IP 192.168.1.1 is blacklisted.
IP 10.0.0.1 is NOT blacklisted.
IP 203.0.113.5 is blacklisted.
