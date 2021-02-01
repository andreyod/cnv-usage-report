# CNV weekly usage Telemeter report

This script will query Telemeter data and produce report for CNV usage.

## Prerequisites:
1. Python 3
2. Prometheus API Client
```bash
pip install prometheus-api-client
```
## How to run:
1. Get access token:
```bash
oc login https://datahub.psi.redhat.com:443 -u <user_name> --password <kerberos_password>
```
2. Export the token as env variable:
```bash
export PROM_ACCESS_TOKEN=`oc whoami -t`
```
3. Execute the script:
```bash
python report.py
```

## Sample output:
"-------------------------------"   
CNV usage weekly 2021-01-31  
"-------------------------------"  

Number of OLM CSVs by version:  
 2.5.3(24, 26%); 2.4.6(21, 23%); 2.4.5(13, 14%); 2.3.0(10, 11%); 2.4.2(6, 7%); 2.4.1(4, 4%); 2.4.4(4, 4%); 2.4.3(3, 3%); 2.2.0(2, 2%); 2.4.0(2, 2%); 2.5.2(2, 2%)

Recent week had 79 domains (running 82 VMs in total, compared to 73 last week):  
sahibinden.com(24); f5.com(10); lmco.com(10); ford.com(7); atos.net(6); ornl.gov(6); amdocs.com(2); dell.com(2); kaloom.com(2); nokia.com(2); ot.olympus.co.jp(2); accenture.com(1); akbank.com(1); ericsson.com(1); express-scripts.com(1); iotos.io(1); juniper.net(1); laposte.net(1); palantir.com(1); samsung.com(1); opennaru.com; utk.edu; kr.af.mil; supermicro.com; netone.co.jp; gmail.com; zf.com; bls.gov; qatarairways.com.qa; 163.com; enfogroup.com; paloaltonetworks.com; dji.minjus.nl; genustechnologies.com; cscinfo.com; mantech.com; inet.co.th; tigera.io; shi-g.com; anadoluefes.com; h3c.com; nti.com.au; datastar.com.ar; spirent.com; soprasteria.com; sympany.ch; cae.com; alcatel-lucent.com; seal.tw; ads.aexp.com; kibs.com.mk; infrasoft.co.kr; hcl.com; slb.com; options-it.com; hepsiburada.com; truist.com; infoblox.com; sct.gouv.qc.ca; prodevans.com; ingrammicro.com; michigan.gov; online.de; ddti.net; cablelabs.com; bet365.com; bancamarch.es; syncrasy.io; hpe.com; aliyun.com; posteitaliane.it; worldline.com; bell.ca; cmbchina.com; diamanti.com; audi.de; criticaltechworks.com; va.gov; ukcloud.com

Added: cae.com kibs.com.mk nti.com.au online.de palantir.com samsung.com sct.gouv.qc.ca shi-g.com

Gone: altibox.no cisco.com optus.com.au
