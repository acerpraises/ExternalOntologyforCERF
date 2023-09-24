import urllib.request, urllib.error, urllib.parse
import json
import os
from pprint import pprint

REST_URL = "http://data.bioontology.org"
API_KEY = "87a6e825-e26c-4bd3-9ff8-508eae699720"

def get_json(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('Authorization', 'apikey token=' + API_KEY)]
    return json.loads(opener.open(url).read())

def print_annotations(annotations, get_class=True):
    for result in annotations:
        class_details = result["annotatedClass"]
        if get_class:
            try:
                class_details = get_json(result["annotatedClass"]["links"]["self"])
            except urllib.error.HTTPError:
                print(f"Error retrieving {result['annotatedClass']['@id']}")
                continue
        print("Class details")
        print("\tid: " + class_details["@id"])
        print("\tprefLabel: " + class_details["prefLabel"])
        print("\tontology: " + class_details["links"]["ontology"])

        print("Annotation details")
        for annotation in result["annotations"]:
            print("\tfrom: " + str(annotation["from"]))
            print("\tto: " + str(annotation["to"]))
            print("\tmatch type: " + annotation["matchType"])

        if result["hierarchy"]:
            print("\n\tHierarchy annotations")
            for annotation in result["hierarchy"]:
                try:
                    class_details = get_json(annotation["annotatedClass"]["links"]["self"])
                except urllib.error.HTTPError:
                    print(f"Error retrieving {annotation['annotatedClass']['@id']}")
                    continue
                pref_label = class_details["prefLabel"] or "no label"
                print("\t\tClass details")
                print("\t\t\tid: " + class_details["@id"])
                print("\t\t\tprefLabel: " + class_details["prefLabel"])
                print("\t\t\tontology: " + class_details["links"]["ontology"])
                print("\t\t\tdistance from originally annotated class: " + str(annotation["distance"]))

        print("\n\n")
def write_annotations(annotations, get_class=True, outputfile="annotate_text_result.txt"):
    # Open the file for writing
    with open(outputfile, "w",encoding="utf-8") as file:
        for result in annotations:
            class_details = result["annotatedClass"]
            if get_class:
                try:
                    class_details = get_json(result["annotatedClass"]["links"]["self"])
                except urllib.error.HTTPError:
                    print(f"Error retrieving {result['annotatedClass']['@id']}")
                    continue
            file.write("Class details")
            file.write("\tid: " + class_details["@id"])
            file.write("\tprefLabel: " + class_details["prefLabel"])
            file.write("\tontology: " + class_details["links"]["ontology"])

            file.write("Annotation details")
            for annotation in result["annotations"]:
                file.write("\tfrom: " + str(annotation["from"]))
                file.write("\tto: " + str(annotation["to"]))
                file.write("\tmatch type: " + annotation["matchType"])

            if result["hierarchy"]:
                file.write("\n\tHierarchy annotations")
                for annotation in result["hierarchy"]:
                    try:
                        class_details = get_json(annotation["annotatedClass"]["links"]["self"])
                    except urllib.error.HTTPError:
                        file.write(f"Error retrieving {annotation['annotatedClass']['@id']}")
                        continue
                    pref_label = class_details["prefLabel"] or "no label"
                    file.write("\t\tClass details")
                    file.write("\t\t\tid: " + class_details["@id"])
                    file.write("\t\t\tprefLabel: " + class_details["prefLabel"])
                    file.write("\t\t\tontology: " + class_details["links"]["ontology"])
                    file.write("\t\t\tdistance from originally annotated class: " + str(annotation["distance"]))

            file.write("\n\n")

text_to_annotate = "Melanoma is a malignant tumor of melanocytes which are found predominantly in skin but also in the bowel and the eye."

# Annotate using the provided text
annotations = get_json(REST_URL + "/annotator?text=" + urllib.parse.quote(text_to_annotate))

# Print out annotation details
write_annotations(annotations)

# Annotate with hierarchy information
annotations = get_json(REST_URL + "/annotator?max_level=3&text=" + urllib.parse.quote(text_to_annotate))
write_annotations(annotations,outputfile="annotate_text_result_hierarchy.txt")

# Annotate with prefLabel, synonym, definition returned
annotations = get_json(REST_URL + "/annotator?include=prefLabel,synonym,definition&text=" + urllib.parse.quote(text_to_annotate))
write_annotations(annotations, False,outputfile="annotate_text_result_notgetClass.txt")
