import sys, time, random
from datetime import datetime, date, timedelta
from Domain.Game import Game

class Trivia(Game):

    def __init__(self):
        super(Trivia,self).__init__()
        self.questionsToAsk = ["Transgenic plants are plants having:", "Bt in popular crop Bt Cotton stands for:", "In transgenics expression of transgene in\ntarget tissue is determined by:", "The DNA used to produce insect resistance transgenic cotton\nis from:", "First biochemical to be produced\ncommercially by microbial cloning and\ngenetic engineering is:", "The bacteria used commercially for the\nfirst time as pesticide is:", "Hirudin is:", "Trichoderma harzianum has proved useful\nmicroorganism for:", "Cry I endotoxins obtained from Bacillus\nthuringiensis are effective against:", "Herbicide resistant GM crops are\nproduced with the main objective to:", "The transgenic species producing human insulin commercially is:", "Antisense technology means:", "The permanent cure for the genetic defect adenosine\ndeaminase (ADA) deficiency is done by:", "Transgenic plants are the ones:", "In developing countries, the problem of night blindness\nis being solved by a transgenic\nfood crop called:", "The enzyme that cuts specifically recognition sites\nin DNA is known as:", "Genetic engineering is possible because:", "The chemical knives of DNAs are:", "When the genotype of an organism is improved\nby the addition of foreign genes,\nthe process is called:", "Recombinant DNA technology can be used to produce\nlarge quantities of biologically active form of\nwhich one of the following products in E. coli?", "One bacterium which has found extensive use\nin genetic engineering work in plants is:", "Eco RI cleaves DNA at:", "The enzyme used in polymerase chain reaction is:", "Identify the plasmid from the following:", "Restriction endonucleases are most widely\nused in recombinant DNA technology.\nThey are obtained from:", "Polymerase chain reaction is most useful in:", "Ligase is used for:", "Gel electrophoresis is used for:", "The linking of antibiotic gene with the\nplasmid vector became possible with:", "The nitrogen bases which pair with two\nhydrogen bonds are", "DNA differs from RNA in", "Extranuclear genetic material is found in", "Which of the following enzyme is required to release the tension\nimposed by uncoiling of strands?", "The enzyme that cuts the bonds of DNA molecule at the origin\nof replication is", "If the strand of DNA has 35 nucleotides, how many \nphosphodiester bonds would exist?", "Formation of mRNA from DNA is called", "Which of the following is not tool of genetic engineering?", "In recombinant\nDNA technology a plasmid vector is cleaved", "-Nif gene- for nitrogen fixation is cereal crops\nlike wheat, etc is introduced by cloning", "What is recombinant DNA?", "What is a transgenic organism?", "Which of the following can happen on its own\nin nature?", "Which of the following is a short segment of\nDNA with -sticky ends-?", "Which is a process that makes more DNA?", "Which of the following will separate segments\nof DNA?", "Which is used for the sequencing of DNA?", "Which of a following is a procedure that\nhas already been successful in the agriculture arena?", "Probes are used in DNA to do which of\nthe following?", "Which is used to get a foreign\ngene into an organism?"]
        self.correctOption = ["Genes of another organism", "Bacillus thuringiensis", "Transgene", "A bacterium", "Human insulin", "Bacillus thuringiensis", "A protein produced from\ntransgenic Brassica napus which\nprevents blood clotting", "Biological control of soil borne\nplant pathogens", "Boll worms", "Eliminate weeds from the\nfield without the use of\nthe manual labour", "Escherichia", "When a piece of RNA that is complementary\nin sequence is used to stop expression\nof a specific gene", "Periodic infusion of genetically\nengineered lymphocytes having\nfunctional ADA and DNA", "Generated by introducing foreign\nDNA into a cell and generating a plant\nfrom that cell", "Golden rice", "Restriction endonuclease", "Restriction endonucleases purified from\nbacteria can be used in vitro", "Endonucleases", "Genetic engineering", "Interferon", "Agrobacterium tumefaciens", "GAATTC", "Taq polymerase", "PBR 322", "Bacterial cell", "DNA amplification", "Joining two DNA\nfragments", "Separation of DNA fragments\naccording to their\nsize", "DNA ligase", "Adenine and thymine", "All others", "Mitochondria and\nplastids", "DNA gyrase", "Endonuclease", "34", "Transcription", "GMO", "The same enzyme that cleave the donor DNA", "Rhizobium meliloti", "All others", "Both", "Both", "RFLP", "PCR", "Both", "Polymer Electrophoresis", "All of these", "All of these", "Both"]
        self.wrongOptionA = ["Genes with no function to perform", "Bacillus tomentosa", "Promoter", "An insect", "Penicillin", "Escherichia coli", "A protein produced by Hordeum\nvulgare, which is rich in lysine", "Bioremediation of contaminated soils", "Nematodes", "Reduce herbicide accumulation\nin food articles for health\nsafety", "Saccharomyces", "RNA polymerse producing DNA", "Administering adenosine deaminase activators", "Produced by somatic embryo in\nartificial medium", "Flavr Savr Tomatoes", "DNA ligase", "Phenomenon of transduction in bacteria\nis understood", "Ligases", "Biotechnology", "Luteining hormone", "Xanthomonas citri", "AAGGTT", "RNA polymerase", "Eco RI", "Bacteriophage", "DNA synthesis", "Separating DNA", "Isolation of DNA molecule", "Exonuclease", "Adenine and cytosine", "Presence of deoxyribose sugar", "Plastid and nucleus", "Endonuclease", "DNA polymerase", "35", "Transformation", "Vectors", "Modified DNA ligase", "Bacillus thuringiensis", "Can be produced in\nbacteria, viruses or yeast", "Plants and animals that express\nDNA that has been modified or\nderived from other species", "Mutations", "PCR", "RFLP", "Gel Electrophoresis", "Gel Electrophoresis", "The addition of DNA into crops\nfor the resistance to diseases", "Highlight repeated\nsegments on genes", "Viruses"]
        self.wrongOptionB = ["Genes in transposition", "Biotechnology", "Reporter", "A wild relative of cotton", "Interferon", "Agrobacterium tumefaciens", "A toxic molecule isolated from\nGossypium hirsutum, which\nreduces human fertility", "Reclamation of wastelands", "Flies", "Eliminate weeds from the field\nwithout the use of herbicides", "Mycobacterium", "A cell displaying a foreign antigen\nused for synthesis of antigens", "Introducing bone marrow cells\nproducing ADA into cells at\nearly embryonic stages", "Produced after protoplast fusion\nin artificial medium", "Stralink maize", "DNA polymerase", "We can see DNA by\nelectron microscope", "Polymerases", "Tissue culture", "Ecdysone", "Bacillus coagulens", "GTATATC", "Ribonuclease", "AIUI", "Plasmids", "Protein synthesis", "DNA polymerase reaction", "Cutting DNA into fragments", "Endonucleases", "Cytosine and guanine", "Presence of thymine base", "Nucleus and cytoplasm", "DNA ligase", "DNA gyrase", "24", "Transduction", "Enzymes", "A heated alkaline solution", "Rhizopus", "Transferable between species", "Also known as Genetically\nModified Organisms (GMOs)", "Recombinants", "STR", "STR", "Polymer Electrophoresis", "Both", "The sterilization of hybrid\ncrops to keep them from\nnaturalizing", "Identify an important\ndisease causing gene", "Bacterial plasmids"]
        self.wrongOptionC = ["No gene", "Best type", "Enhancer", "A virus", "Fertility factor", "Pseudomonas aeruginosa", "Antibiotic produced by a genetically\nengineered bacterium E.coli", "Gene transfer in higher plants", "Mosquitoes", "Encourage eco-friendly herbicides", "Rhizobium", "Production of somaclonal variants\nin tissue cultures", "Enzyme replacement therapy", "Grown in artificial medium after\nhybridization in the field", "Bt Soyabean", "Reverse transcriptase", "We can cut DNA at specific\nsites by endonuclease like DNAase I", "Transcriptases", "Genetic diversity", "Rifamycin", "Clostridium septium", "TATAGC", "Endonuclease", "Hind II", "All prokaryotic cells", "Amino acid synthesis", "All of these", "Construction of recombination DNA\nby joining with closing vectors", "DNA polymerase", "Cytosine and adenine", "Property of replication", "Mitochondria and nucleus", "DNA helicase", "DNA ligase", "70", "Translation", "Foreign DNA", "The different enzyme other\nthan that cleave the\ndonor DNA", "Rhizophora", "DNA that has been altered to contain\ngenes or portions of genes from\ndifferent organisms", "Neither", "Neither", "DNA Fingerprint", "DNA Fingerprint", "Neither", "Neither", "The ability to resist insects\nwith the addition of an enzyme", "Identify a gene that is\nnot functioning correctly", "Neither"]
        self.information = []

    def isOptionCorrect(self, optionSelected):
        return optionSelected == self.correctOption[self.selectedWord]

    def getOptionData(self, optionNumber):
        optionData = ""
        if(optionNumber==1):
            optionData = self.correctOption[self.selectedWord]
        if(optionNumber==2):
            optionData = self.wrongOptionA[self.selectedWord]
        if(optionNumber==3):
            optionData = self.wrongOptionB[self.selectedWord]
        if(optionNumber==4):
            optionData = self.wrongOptionC[self.selectedWord]
        return optionData

    def getRandomOrderOfOptions(self):
        options = "1234"
        orderOfOptions = ""
        randomOrderOptions = []
        listOrderOptions = list(options)
        random.shuffle(listOrderOptions)
        orderOfOptions = orderOfOptions + " " + ''.join(listOrderOptions)
        for eachOption in orderOfOptions:
            if(eachOption.isdigit()):
                randomOrderOptions.append(self.getOptionData(int(eachOption)))
                print("OPTION: ", int(eachOption))
        return randomOrderOptions

    def getCurrentQuestion(self):
        return self.questionsToAsk[self.selectedWord]

    def startTriviaSequence(self):
        self.setRandomPositionOfList(len(self.questionsToAsk))
        optionsToShow = self.getRandomOrderOfOptions()
        return [self.getCurrentQuestion(), optionsToShow[0], optionsToShow[1], optionsToShow[2], optionsToShow[3]]