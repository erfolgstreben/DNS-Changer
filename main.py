import subprocess as _Sub
from typing import Tuple

class DNSConfigurator:
    """
    A Utility Class To Configure DNS Servers For A Given WiFi Interface On Windows.
    Uses The 'netsh' Command To Set Primary And Secondary DNS Servers.

    Example:
        config = DNSConfigurator("Wi-Fi")
        config._dns(DNSConfigurator.CLOUDFLARE)

    Attributes:
        wifi (str): The WiFi Interface Name To Configure.
    """

    CLOUDFLARE: Tuple[str, str] = ("1.1.1.1", "1.0.0.1")
    GOOGLE: Tuple[str, str] = ("8.8.8.8", "8.8.4.4")

    def __init__(
            self, 
            wifi: str
    ) -> None:
        
        self.wifi = wifi

    def _dns(
            self, 
            dns_servers: Tuple[str, str]
    ) -> None:
        
        """
        Set The Primary And Secondary DNS Servers For The Configured WiFi Interface.

        Args:
            dns_servers (Tuple[str, str]): A tuple Containing Primary And Secondary DNS.
        """

        dns1, dns2 = dns_servers

        try:
            _Sub.run(
                [
                    "netsh", "interface", "ipv4", "set", "dnsservers",
                    f"name={self.wifi}", "static", dns1, "primary"
                ],

                check=True
            )

            _Sub.run(
                [
                    "netsh", "interface", "ipv4", "add", "dnsservers",
                    f"name={self.wifi}", dns2, "index=2"
                ],
                check=True
            )

            print(
                f"Success - DNS For '{self.wifi}' Set To {dns1} And {dns2}"
            )

        except _Sub.CalledProcessError as e:
            print(
                f"Failure - Failed To Set DNS For '{self.wifi}': " + str(e)
            )


if __name__ == "__main__":
    choice: str = input(
        "Use Cloudflare or Google [C/G]: "
    ).strip(

    ).upper(

    )

    configurator = DNSConfigurator(
        input(
            "Enter Your WiFi's Name: "
        ).strip(

        )
    )

    match choice:

        case "C":
            configurator._dns(
                DNSConfigurator.CLOUDFLARE
            )

        case "G":
            configurator._dns(
                DNSConfigurator.GOOGLE
            )

        case _:
            print(
                "Error - Please Choose 'C' Or 'G'"
            )