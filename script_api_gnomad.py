from string import Template
import pysam
import pandas as pd 
import csv

class GnomadS3API():
    url_template = Template("https://gnomad-public-us-east-1.s3.amazonaws.com/release/${version}/vcf/${scope}/gnomad.${scope}.v${version}.sites.chr${chromosome}.vcf.bgz")
    

    @classmethod
    def get_variant_gnomad_freqs_json(cls, chrom,pos, gnomad_version, scope="exomes"): #can also be genomes
        # Get variants on reference builds in a dict
       
        # Load the tabix index for that variant from the S3 URL
        vcf = pysam.VariantFile(
            cls.url_template.substitute(
                {
                    "version": gnomad_version,
                    "scope": scope,
                    "chromosome": chrom,

                }
            )
        )

        # Query the ROI
        records = vcf.fetch(
            f"chr{chrom}", 
            pos - 1, 
            pos,
        )

        # Iterate over the record and find the record of interest
        record_list = []
        for record in records:
            item = {}
            item["AC"] = record.info["AC"]
            item["AN"] = record.info["AN"]
            item["nhomalt"] = record.info["nhomalt"]
            item ["AF"] = record.info["AF"]
            record_list.append(item)
            #print(item)
        print(record_list)


                # print(record.alts ,
                #        "AC=", record.info["AC"],
                #        "AN=",record.info["AN"],
                #        "nhomalt=", record.info["nhomalt"],
                #        "AF=", record.info["AF"])

        # Serialise the VCF record into JSON and return it
    @classmethod
    def get_variant_gnomad_freqs_json_into_excel(cls,file): #can also be genomes
        # Get variants on reference builds in a dict

        with open(file, "r", encoding="utf-8-sig") as datafile:
            targets = csv.DictReader(datafile)
            #print(targets.fieldnames)
            df_input_data = pd.DataFrame.from_dict(targets)


            gnomad_version = "4.0"
            scope="genomes"
            #df_results = pd.DataFrame(columns=["chrom","pos","ref", "alt", "AC", "AN", "nhomalt", "AF"])'1', '2', '3', '4', '5', '6', '7', '8', '9', 
            for chrom in ['10',
                      '11', '12', '13', '14', '15', '16', '17', '18', '19',
                      '20', '21', '22', 'X', 'Y']:
                print(f"starting {chrom} analysis")
                
                #filter Pd df down to chroms currently searching. 
                current_chrom_match = df_input_data[df_input_data.iloc[:,3]== str(chrom)]

                # Load the tabix index for that variant from the S3 URL
                vcf = pysam.VariantFile(
                    cls.url_template.substitute(
                        {
                            "version": gnomad_version,
                            "scope": scope,
                            "chromosome": chrom,
                
                        }
                    )
                )
                
                #empty record list
                record_list = []
                
                #loop through the pandas dataframe
                for index, row in current_chrom_match.iterrows():
                    
                    records = vcf.fetch(
                        f"chr{chrom}", 
                        int(row["Coordinates"]) - 1, 
                        int(row["Coordinates"]),
                    )
                    print (index)
                    for record in records:
                        if row["alt"] in record.alts:
                            item = {}
                            item["chrom"] = record.chrom
                            item["pos"] = record.pos
                            item["ref"] = record.ref
                            item["alt"] = record.alts
                            item["AC"] = record.info["AC"]
                            item["AN"] = record.info["AN"]
                            item["nhomalt"] = record.info["nhomalt"]
                            item["AF"] = record.info["AF"]
                            record_list.append(item)
                        else:
                            pass

                new_rows= pd.DataFrame.from_dict(record_list)
                new_rows.to_csv("output_genomes.csv", index= False, mode= 'a' )
                print(f"complete for chrom {chrom}")
               # df_results = pd.concat([df_results, new_rows], ignore_index= True)
            #df_results.to_csv("output.csv", index= False )



        
    
 

# GnomadS3API.get_variant_gnomad_freqs_json(chrom=3, pos=125084066, gnomad_version="4.0")
GnomadS3API.get_variant_gnomad_freqs_json_into_excel("csv for gnomad.csv")
"""
Rob is providing an excel file with all those variants with chrom ref and alt and position 
i will go 
"""
