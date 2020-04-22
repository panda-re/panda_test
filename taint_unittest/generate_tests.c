#include <stdio.h>
#include <stdlib.h>

int bin_test_floating[10] = {1, 1, 1, 1, 0, 0, 0, 0, 0, 0};
char *bin_names[10] = {"add", "sub", "mul", "div", "mod", "bwand", "bwor", "bwxor", "bwsl", "bwsr"};
char *bin_ops[10] = {"+", "-", "*", "/", "%", "&", "|", "^", "<<", ">>"};

int un_test_floating[1] = {0};
char *un_names[] = {"bwnot"};
char *un_ops[] = {"~"};

int signedness[10] = {0, 0, 0, 0, 1, 1, 1, 1, 0, 0};
char *types[10] = {"uint8", "uint16", "uint32", "uint64", "int8", "int16", "int32", "int64", "float", "double"};
const int end_int_types = 8;
const int end_all_types = 10;

int main(int argc, char **argv) {

    // bin tests
    for(int i=0;i<10;i++) {
        int type_loop_end = end_int_types;
        if(bin_test_floating[i] != 0) {
            type_loop_end = end_all_types;
        }
        for(int j=0;j<type_loop_end;j++) {
        char fname[64];
        FILE *cfile;
        if(signedness[j] != 0) {
            sprintf(fname, "./src/%s_s%s.c", bin_names[i], types[j]);
        }
        else {
            sprintf(fname, "./src/%s_%s.c", bin_names[i], types[j]);
        }
        cfile = fopen(fname, "w+");
        fprintf(cfile, "#include \"taint.h\"\n");
        fprintf(cfile, "#define the_op %s\n", bin_ops[i]);
        if(j < end_int_types) {
            fprintf(cfile, "#define the_type %s_t\n", types[j]);
        }
        else {
            fprintf(cfile, "#define the_type %s\n", types[j]);
        }
        fprintf(cfile, "#define x_LABEL 0xCCCCCCCC\n");
        fprintf(cfile, "#define y_LABEL 0xDDDDDDDD\n");
        fprintf(cfile, "int main(int argc, char **argv) {\n");
        fprintf(cfile, "    the_type x = (the_type)1;\n");
        fprintf(cfile, "    the_type y = (the_type)2;\n");
        fprintf(cfile, "    the_type z = (the_type)0;\n");
        fprintf(cfile, "    panda_taint_label_buffer(&x, x_LABEL, sizeof(the_type));\n");
        fprintf(cfile, "    panda_taint_label_buffer(&y, y_LABEL, sizeof(the_type));\n");
        fprintf(cfile, "    panda_taint_assert_label_found_range(&x, sizeof(the_type), x_LABEL);\n");
        fprintf(cfile, "    panda_taint_assert_label_found_range(&y, sizeof(the_type), y_LABEL);\n");
        fprintf(cfile, "    panda_taint_assert_label_not_found_range(&z, sizeof(the_type), x_LABEL);\n");
        fprintf(cfile, "    panda_taint_assert_label_not_found_range(&z, sizeof(the_type), y_LABEL);\n");
        fprintf(cfile, "    z = x the_op y;\n");
        fprintf(cfile, "    panda_taint_assert_label_found_range(&z, sizeof(the_type), x_LABEL);\n");
        fprintf(cfile, "    panda_taint_assert_label_found_range(&z, sizeof(the_type), y_LABEL);\n");
        fprintf(cfile, "    return 0;\n");
        fprintf(cfile, "}\n");
        fprintf(cfile, "\n");
        fclose(cfile);
        }
    }

    // un tests
    for(int i=0;i<1;i++) {
        int type_loop_end = end_int_types;
        if(un_test_floating[i] != 0) {
            type_loop_end = end_all_types;
        }
        for(int j=0;j<type_loop_end;j++) {
        char fname[64];
        FILE *cfile;
        if(signedness[j] != 0) {
            sprintf(fname, "./src/%s_s%s.c", un_names[i], types[j]);
        }
        else {
            sprintf(fname, "./src/%s_%s.c", un_names[i], types[j]);
        }
        cfile = fopen(fname, "w+");
        fprintf(cfile, "#include \"taint.h\"\n");
        fprintf(cfile, "#define the_op %s\n", un_ops[i]);
        if(j < end_int_types) {
            fprintf(cfile, "#define the_type %s_t\n", types[j]);
        }
        else {
            fprintf(cfile, "#define the_type %s\n", types[j]);
        }
        fprintf(cfile, "#define x_LABEL 0xCCCCCCCC\n");
        fprintf(cfile, "int main(int argc, char **argv) {\n");
        fprintf(cfile, "    the_type x = (the_type)1;\n");
        fprintf(cfile, "    the_type z = (the_type)0;\n");
        fprintf(cfile, "    panda_taint_label_buffer(&x, x_LABEL, sizeof(the_type));\n");
        fprintf(cfile, "    panda_taint_assert_label_found_range(&x, sizeof(the_type), x_LABEL);\n");
        fprintf(cfile, "    panda_taint_assert_label_not_found_range(&z, sizeof(the_type), x_LABEL);\n");
        fprintf(cfile, "    z = the_op(x);\n");
        fprintf(cfile, "    panda_taint_assert_label_found_range(&z, sizeof(the_type), x_LABEL);\n");
        fprintf(cfile, "    return 0;\n");
        fprintf(cfile, "}\n");
        fprintf(cfile, "\n");
        fclose(cfile);
        }
    }

    return 0;
}
