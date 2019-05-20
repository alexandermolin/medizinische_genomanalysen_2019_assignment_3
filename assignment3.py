#! /usr/bin/env python3

import vcf
import httplib2

__author__ = 'Alexander Molin'

##
## Aim of this assignment is to annotate the variants with various attributes
## We will use the API provided by "myvariant.info" - more information here: https://docs.myvariant.info
## NOTE NOTE! - check here for hg38 - https://myvariant.info/faq
## 1) Annotate the first 900 variants in the VCF file
## 2) Store the result in a data structure (not in a database)
## 3) Use the data structure to answer the questions
##
## 4) View the VCF in a browser
##

class Assignment3:

    def __init__(self):
        ## Check if pyvcf is installed
        print("PyVCF version: %s" % vcf.VERSION)

        ## Call annotate_vcf_file here
        self.vcf_path = "chr16.vcf"

    def annotate_vcf_file(self, filename):
        '''
        - Annotate the VCF file using the following example code (for 1 variant)
        - Iterate of the variants (use first 900)
        - Store the result in a data structure
        :return:
        '''

        ## Build the connection
        h = httplib2.Http()
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        params_pos = []  # List of variant positions
        with open(self.vcf_path) as myVCF:
            vcf_reader = vcf.Reader(myVCF)
            for counter, record in enumerate(vcf_reader):
                params_pos.append(record.CHROM + ":g." + str(record.POS) + record.REF + ">" + str(record.ALT[0]))

                if counter >= 899:
                    break

        ## Build the parameters using the list we just built
        params = 'ids=' + ",".join(params_pos) + '&hg38=true'

        ## Perform annotation
        res, con = h.request('http://myvariant.info/v1/variant', 'POST', params, headers=headers)
        annotation_result = con.decode('utf-8')

        with open(f"{filename}.json", "w") as af:
            for line in annotation_result:
                af.write(line)

    def get_list_of_genes(self):
        '''
        Print the name of genes in the annotation data set
        :return:
        '''

        gene_names = []
        with open("annotation.json", "r") as annot:
            for line in annot:
                if "genename" in line:
                    gene_names.append(line)

        gene_names = set([i.strip().strip(",").strip('"genename": ').strip('"') for i in gene_names])
        gene_amount = len(gene_names)
        print(f"\nNumber of genes that were found: ", gene_amount)
        print(f"\nGene names: {gene_names}")


    def get_num_variants_modifier(self):
        '''
        Print the number of variants with putative_impact "MODIFIER"
        :return:
        '''

        modifier = 0
        with open("annotation.json", "r") as annot:
            for line in annot:
                if '"putative_impact": "MODIFIER"' in line:
                    modifier += 1
        print(f"\nVariants with putative impact = modifier: {modifier}")

    def get_num_variants_with_mutationtaster_annotation(self):
        '''
        Print the number of variants with a 'mutationtaster' annotation
        :return:
        '''

        mutation_taster = 0
        with open("annotation.json", "r") as annot:
            for line in annot:
                if "mutationtaster" in line:
                    mutation_taster += 1

        print(f"\nVariants with mutationtaster annotation: {mutation_taster}")

    def get_num_variants_non_synonymous(self):
        '''
        Print the number of variants with 'consequence' 'NON_SYNONYMOUS'
        :return:
        '''

        num_nonsyn = 0
        with open("annotation.json", "r") as annot:
            for line in annot:
                if '"consequence": "NON_SYNONYMOUS"' in line:
                    num_nonsyn += 1
        print(f"\nVariants with consequence = non-synonymous: {num_nonsyn}")

    def view_vcf_in_browser(self):
        '''
        - Open a browser and go to https://vcf.iobio.io/
        - Upload the VCF file and investigate the details
        :return:
        '''

        ## Document the final URL here
        print(f"\nResults: https://vcf.iobio.io/?species=Human&build=GRCh38")

    def print_summary(self):
        self.annotate_vcf_file("annotation")
        self.get_list_of_genes()
        self.get_num_variants_modifier()
        self.get_num_variants_with_mutationtaster_annotation()
        self.get_num_variants_non_synonymous()
        self.view_vcf_in_browser()



def main():
    print("Assignment 3")
    assignment3 = Assignment3()
    assignment3.print_summary()
    print(f"\nDone with assignment 3")


if __name__ == '__main__':
    main()
