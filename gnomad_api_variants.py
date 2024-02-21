from string import Template
import pysam

class GnomadS3API():
    url_template = Template("https://gnomad-public-us-east-1.s3.amazonaws.com/release/${version}/vcf/${scope}/gnomad.${scope}.v${version}.sites.chr${chromosome}.vcf.bgz")
    

    @classmethod
    def get_variant_gnomad_freqs_json(cls, chrom,pos, gnomad_version, scope="genomes"):
        # Get variants on reference builds in a dict
       
        # Load the tabix index for that variant from the S3 URL
        url = cls.url_template.substitute(
                {
                    "version": gnomad_version,
                    "scope": scope,
                    "chromosome": chrom,
                }
            )
    
        vcf = pysam.TabixFile(
            url
        )

        # Query the ROI
        records = vcf.fetch(
            f"chr{chrom}", 
            (pos - 1), 
            (pos),
        )

        # Iterate over the record and find the record of interest
        for record in records:
            print(record)

        # Serialise the VCF record into JSON and return it


GnomadS3API.get_variant_gnomad_freqs_json(chrom="1", pos=112312, gnomad_version="4.0")