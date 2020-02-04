@APP.get("/averages/{language}")
async def get_average_lengths_by_file(
    language: str
):
    """
    This is not used at the frontend but is used to calculate
    average word length per file to determine authenticity
    """
    database = get_db()
    query_files_list = database.AQLQuery(
        query=QUERY_FILES_FOR_LANGUAGE,
        batchSize=100000,
        bindVars={"language": language},
    )

    filelist = []
    for file in query_files_list.result:
        filelist.append(file["filename"])

    averages = {}
    total_collection_dict = {}
    for filename in filelist:
        # comment out the if-statement if you want all files
        # if filename.startswith("atk-abh01a1"):
            [totalcharacters, totalwordcount] = calculate_average(filename)
            if totalwordcount > 0:
                averages[filename] = round(totalcharacters/totalwordcount, 2)
            else:
                averages[filename] = 0
            collection_key = re.search(COLLECTION_PATTERN, filename)
            if not collection_key:
                continue

            collection = collection_key.group()
            if collection not in total_collection_dict.keys():
                total_collection_dict[collection] = [totalcharacters, totalwordcount]
            else:
                total_collection_dict[collection][0] += totalcharacters
                total_collection_dict[collection][1] += totalwordcount

    collection_averages = {}
    for key, value in total_collection_dict.items():
        collection_averages[key] = round(value[0]/value[1], 2)

    # The following sorts values in ascending order
    # return {k: v for k, v in sorted(averages.items(), key=lambda item: item[1])}, {k: v for k, v in sorted(collection_averages.items(), key=lambda item: item[1])}
    return averages, collection_averages


QUERY_ALL_SEGMENT_TEXTS = """
    FOR file IN files
        FILTER file.filename == @filename
        FOR segmentnr IN file.segmentnrs
            FILTER REGEX_TEST(segmentnr, ":[1-9]")
            FOR segment in segments
                FILTER segment._key == segmentnr
                RETURN segment.segtext
"""


def calculate_average(filename):
    database = get_db()
    query_segment_texts = database.AQLQuery(
        query=QUERY_ALL_SEGMENT_TEXTS,
        batchSize=100000,
        bindVars={"filename": filename},
    )
    header_pattern = r"vagga$|nikāya$| Nikāya |sutta$|[Nn]ipāta$|^Dhammapada$|[nN]iddesa$|vaggagāthā$|^[a-zāīṇṅA-Z]+ [0-9]+$|vimāna$|vatthu$|piṭake$"

    totalwordcount = 0
    totalcharacters = 0

    for line in query_segment_texts.result:
        if re.search(header_pattern,line.strip()):
            continue
        if not re.search(r"^tika|^anya|^atk", filename) and re.search(r"^[0-9]", line):
            continue
        if line == query_segment_texts.result[0] and not re.search(r"^[md]n[0-9]|^pli|^tika|^anya|^atk", filename):
            continue
        line = re.sub(r"[0-9-_\?!\.,:;\|\"\'\{\}\[\]\(\)&\#‘“”’…–—☑»«⇒]", "", line)
        line = re.sub(r"  ", " ", line)
        line = re.sub(r" pe |^pe | pe$", " ", line)
        totalwordcount += len(line.split())
        totalcharacters += len(line.replace(" ",""))
    return [totalcharacters, totalwordcount]