
# RGB  (Redfish Green500 Benchmarker) 
## (A Green500 Benchmark Tool Using Redfish Technology)


### 1- Overview


The goal of this research study is to develop and demonstrate methods to automate benchmarking the energy efficiency of high performance computing systems based on the Green500 methodology via direct measurements obtained from the baseboard management controllers using Redfish standard, instead of via an external power meter and a manual process. To achieve this goal, we design and develop an automatic Green500 benchmark tool based on Redfish, called RGB (Redfish Green500 Benchmarker). This tool also evaluates implementations of the Redfish standard to determine their ability to meet the requirements of the Green500 benchmarking protocols.



## 2-How To use the application:
###  Step 1: Make sure you have the following python libraries.

	
    • requests
    • socket
    • ipaddress
    • json
    • datetime
    • random
    • time
    • threading
    • sys
    • colorama
    • termcolor 
    • pyfiglet 
    • cs 


You can use one of the following commands to install a package if you do not have it.

    • python -m pip install package-name
    • pip install --user package-name
    • python3 -m pip install package-name
    • pip3 install --user package-name

Also, it needs to be run by  Python 3.6.8 or above.
###  Step 2: Make sure you have the Linpack Benchmark on your system, and run it with the application.


### Step 3: Run the Application.

    • Create a file that contains a list of the IP addresses of the cluster facilities.
    • For Level1 and Level2 of the Green500 benchmarking, run the following command:
        python3  RGB.py 
    • For Level3 of the Green500 benchmarking, you can run a simulated test using the docker images in elham1296 repository in the dockerhub.
        docker pull elham1296/telemetry
		docker pull elham1296/rgb-listener
		docker pull elham1296/rgb-node
  



## 3- Demo

Please visit the following presentation links and accompanying videos that show how to use the application.

    • Demo: https://www.youtube.com/watch?v=Rikst5cL18A

    • Presentation: https://sc18.supercomputing.org/proceedings/tech_poster/poster_files/post254s2-file2.pdf

    • Paper: https://ieeexplore.ieee.org/document/9289729
		   



## 4- Acknowledgments

This research is supported by the Cloud and Autonomic Computing site and High Performance Computing Center at Texas Tech University and the collaboration with Dell Inc., and DMTF.   Many thanks to Mr. [Jon Hass](https://github.com/JonHass), Dr. [Alan Sill](https://github.com/alansill), Mr. [Opeyemi Openiyi](https://github.com/doubleope)  and Dr. [Yong Chen](https://www.depts.ttu.edu/cs/faculty/yong_chen/index.php)  for their guidance, help and support. 


## 5-Support or Contact

If you have any question about that please contact [Elham Hojati](https://github.com/El-H-git)(For the benchmarker), and  Mr. [Opeyemi Openiyi](https://github.com/doubleope)(for the RGB-GUI).





## 6- References

[1] https://www.dmtf.org/standards/redfish

[2] https://www.top500.org/lists/green500/

[3] https://sc18.supercomputing.org/proceedings/tech_poster/poster_files/post254s2-file2.pdf

[4] https://ieeexplore.ieee.org/document/9289729



