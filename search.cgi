#!/usr/local/bin/python3

import jinja2
import re
import mysql.connector
import cgi
import cgitb
cgitb.enable()

# This line tells the template loader where to search for template files
templateLoader = jinja2.FileSystemLoader( searchpath="./templates" )

# This creates your environment and loads a specific template
env = jinja2.Environment(loader=templateLoader)
template = env.get_template('results.html')

form = cgi.FieldStorage()
gene = form.getfirst('search')
#gene = "bifunctional"
def main(search):
	conn = mysql.connector.connect(user='ldorse13', password='Mpbg2006', host='localhost', database='ldorse13_chado')
	curs = conn.cursor()
	qry = "SELECT f.uniquename AS protein, product.value AS gene_product FROM feature f JOIN cvterm polypeptide ON f.type_id=polypeptide.cvterm_id JOIN featureprop product ON f.feature_id=product.feature_id JOIN cvterm productprop ON product.type_id=productprop.cvterm_id WHERE polypeptide.name = 'polypeptide' AND productprop.name = 'gene_product_name' AND product.value LIKE %s";
	curs.execute(qry, ('%' + str(search) + '%', ))
	proteins = list()
	products = list()
	for protein, gene_proudct in curs:
		proteins.append(protein.decode('UTF-8'))
		products.append(gene_proudct.decode('UTF-8'))
	print(proteins)
	print(products)
	#results = list()
	print("Content-Type: text/html\n\n")
	print(template.render(res = zip(proteins, products)))
	#print("Protein         Gene Product")
	#for (protein, gene_product) in curs:
	#	print(protein.decode('UTF-8') + "	" + gene_product.decode('UTF-8') + "\n")
	conn.close()
	
if __name__ == '__main__':
	main(gene)


#print("Content-Type: text/html\n\n")
#print(template.render(res = results))
