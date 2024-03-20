import replicate


def generate_LLama_response(prompt):
    # The run method takes the model name and input parameters.
    output = replicate.run(
        "meta/codellama-70b-instruct:a279116fe47a0f65701a8817188601e2fe8f4b9e04a518789655ea7b995851bf",
        input={
            "top_k": 10,
            "top_p": 0.95,
            "prompt": prompt,
            "max_tokens": 5000,
            "temperature": 0.8,
            "system_prompt": "You are an AI that will create java junit tests for the lines of a code that are not "
                             "covered. You are going to receive the code and the numbered lines that are not covered for the "
                             "tests, then you will return the tests to cover that lines, the code will be always on java, "
                             "and you would return just the code and nothing else, don't add any comments or anything like "
                             "that even if you think there is something wrong. I repeat, dont add comments, just return the "
                             "code. Also you would add the word 'generated' to the name of the class that you are "
                             "going to return. For example, if the class name is 'Numbers', you would return 'NumbersGenerated'.",
            "repeat_penalty": 1.1,
            "presence_penalty": 0,
            "frequency_penalty": 0
        }
    )
    response = ""
    for item in output:
        response = response + item
    print(response)
    return response


prompt = ("The code below is missing test coverage for the following lines: 3," +
"Write the tests to cover the lines above from this code: ." +
"package temp; " +
"public class NoteMarker {" +
          "   public static String checkNotes(int notes){" +
          "       String result = "";" +
          "     if(notes>=0 && notes<4){" +
          "     result = \"fail\";" +
"   }else if(notes>=4 && notes < 6){" +
"       result = \"second class\";" +
"    }else if(notes >= 6 && notes <=10){" +
"       result = \"first class\";" +
"    }else{" +
"        result = \"incorrect number\";" +
"     }" +
"     return result;" +
"  }" +
"}")



# print(generate_LLama_response(prompt))
# The meta/codellama-70b-instruct model can stream output as it's running.
# The predict method returns an iterator, and you can iterate over that output.
# for item in output:
#     # https://replicate.com/meta/codellama-70b-instruct/api#output-schema
#     print(item, end="")
