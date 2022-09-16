#!/usr/bin/env bash
FUNCTION=function.zip
FUNCTION2=error_parser.zip
cd function1/package/
zip -r9 ../../$FUNCTION .
cd ..
#zip -g ../$FUNCTION lambda_function.py
#zip -g ../$FUNCTION git-2.4.3.tar lambda_function.py
zip -g ../$FUNCTION id_rsa lambda_function.py
cd ..
cd function2/
zip -g ../$FUNCTION2 lambda_function.py
