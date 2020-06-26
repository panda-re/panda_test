# panda_test

Regression and other tests for PANDA. These run as part of the [current CI](https://github.com/panda-re/panda/tree/master/.github/workflows).
If your PR is failing the CI and you're like to replicate the tests locally to debug (assuming you've [built PANDA and installed PyPANDA](https://github.com/panda-re/panda/blob/master/panda/python/docs/USAGE.md#installation), and run `pip install -r requirements.txt`):

### QEMU Checks

```bash
cd panda/  # Main PANDA repo, not this repo!
mkdir -p build/
cd build/
export PANDA_TEST=yes
bash ../build.sh <target_name>  # E.g. target_name == arm-softmmu
```

### Regression Tests

```
export PANDA_REGRESSION_DIR=$(realpath panda_test/regdir)
cd panda/panda/testing  # Main PANDA repo, not this repo!
python3 ptest.py test
```

### Taint Unit Tests

```bash
cd panda_test/tests/taint2/
python3 taint2_multi_arch_record_or_replay.py --arch <arch_name> --mode record # E.g. <arch_name> == x86_64
python3 taint2_multi_arch_record_or_replay.py --arch <arch_name> --mode replay
python3 taint2_multi_arch_record_or_replay.py --arch <arch_name> --mode check
```
