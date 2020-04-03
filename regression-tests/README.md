# PANDA Regression Tests

These tests are intended to be full system tests for PANDA.

# Running the Tests

1. Run the included test data download script to obtain the entire test data
   set.

    ```
    TODO
    ```

2. Setup a virtualenv with the Python dependencies used for testing.

    ```
    python3 -m virtualenv -p /usr/bin/python3 env
    . ./env/bin/activate
    pip3 install -r requirements.txt
    ```

3. Execute the tests.

    ```
    ./run.py /path/to/PANDA/build/folder /path/to/folder/containing/test/data
    ```

4. Once you've run the tests, you can deactivate the virtualenv.

    ```
    deactivate
    ```

# Adding Tests

Adding tests to the regression test suite is easy. Just create a new Python
module under the tests directory with the prefix `test_`. The test framework
will automatically resolve tests.

A test must have a `run` and `cleanup` method. `run` returns true if the test
passes or false if it fails. Refer to the examples directory.
