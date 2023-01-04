
import requests
import json
#This is the URL
url='https://gnomad.broadinstitute.org/api'
#user prompt for the gene name
Gene_name=input("whats is the gene you are looking at? ")
#This is the Query thats sent to the graphql api
gene1=("""
{
        gene(gene_symbol:"%s", reference_genome: GRCh37) {
    chrom
    name
    gnomad_constraint {
      syn_z
      mis_z
      pLI
    }
  }
}
"""%(Gene_name))
# the string variable allows a gene to be requested
print("so your looking for This info on  "+Gene_name+"?")
#This is the Query for GNomad graphql API, using the requests module. the word 
prompt = requests.post(url=url, json={"query": gene1})
print(" status code: ", prompt.status_code)
#status code 200 means success, 400 means something has gone wrong. 
if prompt.status_code == 200:
  list=json.loads(prompt.text) 
  print(json.dumps(list, indent=4))
syn_z=(list["data"]["gene"]["gnomad_constraint"]["syn_z"])
mis_z=(list["data"]["gene"]["gnomad_constraint"]["mis_z"])
pLI=(list["data"]["gene"]["gnomad_constraint"]["pLI"])
chrom=(list["data"]["gene"]["chrom"])
name=(list["data"]["gene"]["name"])
print("""Gene is found on chromosome %s and its full title is:' %s '.
 Based off Gnomad-data the %s has the following constraints""" %(str(chrom),name, Gene_name))
if syn_z <= 1:
    print("This gene is highly resistant to synonymous variants")
elif syn_z >=3:
    print("This gene is highly susceptible to synonymous variants")
else : 
    print("synonymous variants will likely have some affect ")
if mis_z <= 1:
    print("This gene is highly resistant to missense variants")
elif syn_z >=3:
    print("This gene is highly susceptible to missense variants")
else : 
    print("missense variants will likely have some affect ")
