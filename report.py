import os
import datetime
import prometheus_api_client
import requests

requests.packages.urllib3.disable_warnings()

url = os.environ.get("PROM_URL", "https://telemeter-lts.datahub.redhat.com")
try:
    token = os.environ["PROM_ACCESS_TOKEN"]
except KeyError:
    print("Obtain PROM_ACCESS_TOKEN from a login to https://datahub.psi.redhat.com/console/catalog")
    raise

print("-------------------------------")
print("CNV usage weekly", datetime.date.today())
print("-------------------------------\n")

pc = prometheus_api_client.PrometheusConnect(url=url, headers={"Authorization": "bearer {}".format(token)}, disable_ssl=True)

def weekly_email_domains(pc, end_time):
    q = """count by (email_domain)((subscription_sync_total{installed=~"kubevirt-hyperconverged.*"}) + on (_id) group_left(email_domain)( 0 * topk by (_id) (1, subscription_labels{email_domain!~"redhat.com|.*ibm.com"})))"""
    v = pc.custom_query_range(
            query=q,
            start_time=end_time - datetime.timedelta(days=7),
            end_time=end_time, step='1h')
    return frozenset(map(lambda x: x['metric']['email_domain'], v))

def get_percentage(part, whole):
    percentage = 100 * float(part)/float(whole)
    return "{:.1f}".format(percentage)

def running_vms(pc, end_time):
    q = """sum(cnv:vmi_status_running:count + on (_id) group_left(_blah) (0 * group by (_id, email_domain) (id_version_ebs_account_internal:cluster_subscribed{internal=""})) + 0)"""
    v = pc.custom_query_range(
            query=q,
            start_time=end_time - datetime.timedelta(days=7),
            end_time=end_time, step='1h')
    current = v[-1]['values'][-1][-1]
    last_week = v[-1]['values'][0][-1]
    return "(running " + current + " VMs in total, compared to " + last_week + " last week):"

def csvs_by_version(pc, end_time):
    end_time = datetime.datetime.now()
    q = """sort_desc ((count by (version) (csv_succeeded{name=~".*hyperconverged.*"} + on (_id) group_left(_blah) (0 * group by (_id, email_domain) (id_version_ebs_account_internal:cluster_subscribed{internal=""})) + 0)))"""
    v = pc.custom_query_range(
            query=q,
            start_time=end_time - datetime.timedelta(hours=3),
            end_time=end_time, step='1h')
    d = dict(map(lambda x: (x['metric']['version'], int(x['values'][-1][-1])), v))
    sorted_csvs = sorted(d.items(), key=lambda i: i[1], reverse=True)
    total = sum(d.values())
    print_string = ""
    for i, v in enumerate(sorted_csvs):
        if i != 0:
            print_string = print_string + "; "
        print_string = print_string+v[0]+"("+str(v[1])+", "+str(round(float(get_percentage(v[1], total))))+"%"+")"
    return print_string

def vms_by_domain(pc, end_time, all_domains):
    q = """sort_desc(sum by (email_domain)(cnv:vmi_status_running:count + on (_id) group_left(_blah) (0 * group by (_id) (id_version_ebs_account_internal:cluster_subscribed{internal=""}))+ on (_id) group_left(email_domain) (0 * topk by (_id) (1, subscription_labels{}))))"""
    v = pc.custom_query_range(
            query=q,
            start_time=end_time - datetime.timedelta(hours=3),
            end_time=end_time, step='1h')
    domains_with_vms = frozenset(map(lambda x: x['metric']['email_domain'], v))
    domains_without_vms = recent - domains_with_vms
    d = dict(map(lambda x: (x['metric']['email_domain'], int(x['values'][-1][-1])), v))
    domains_with_vms = sorted(d.items(), key=lambda i: i[1], reverse=True)
    print_string = ""
    for i, v in enumerate(domains_with_vms):
        if i != 0:
            print_string = print_string + "; "
        print_string = print_string + v[0] + "(" + str(v[1]) + ")"
    for v in domains_without_vms:
        print_string = print_string + "; " + v
    return print_string


now = datetime.datetime.now()
print("Number of OLM CSVs by version:\n", csvs_by_version(pc, now))
recent = weekly_email_domains(pc, now)
print("\nRecent week had {} domains".format(len(recent)), running_vms(pc, now))
print(vms_by_domain(pc, now, recent), "\n")
previous = weekly_email_domains(pc, now - datetime.timedelta(days=7))
print("Added:", ' '.join(sorted(recent - previous)), "\n")
print("Gone:", ' '.join(sorted(previous - recent)))
