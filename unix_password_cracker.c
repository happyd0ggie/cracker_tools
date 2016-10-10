#ifndef _XOPEN_SOURCE
#define _XOPEN_SOURCE
#endif
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <ctype.h>

char *crack(char *password, char *dictonary);
void get_user_name_and_hashed_password(char *s, char *user, char *hashed_password);
static inline void usage(char *prog);

int main(int argc, char **argv)
{
    char *password_file = NULL;
    char *dictonary_file = NULL;
    char *optstr = "f:d:h";
    int c;

    while ((c = getopt(argc, argv, optstr)) != -1)
    {
        switch (c)
        {
        case 'f':
            password_file = optarg;
            break;
        case 'd':
            dictonary_file = optarg;
            break;
        case 'h':
            usage(*argv);
            break;
        default:
            abort();
        }
    }

    if (argc < 5)
    {
        usage(*argv);
        exit(-1);
    }

    crack(password_file, dictonary_file);

    return 0;
}

char *crack(char *password_file, char *dictonary_file)
{
    FILE *password_fp = fopen(password_file, "r");
    FILE *dictonary_fp = fopen(dictonary_file, "r");
    char user[512];
    char hashed_password[1024];
    char line[4096];
    char password[512];
    char salt[13];
    int found;

    if (!password_fp || !dictonary_fp)
    {
        perror("open():");
        exit(-1);
    }

    while (fgets(line, sizeof(line), password_fp) != NULL)
    {
        get_user_name_and_hashed_password(line, user, hashed_password);
        if (strcmp(hashed_password, "*") != 0 && strcmp(hashed_password, "!") != 0)
        {
            fprintf(stdout, "[*] Cracking password for %s...\n", user);
            found = 0;
            while (fscanf(dictonary_fp, "%s", password) != EOF && !found)
            {
                strncpy(salt, hashed_password, 12);
                salt[12] = '\0';
                //fprintf(stdout, "%s,%s,%s,%s", user, hashed_password, password, salt);
                //getchar();
                if (strcmp(crypt(password, salt), hashed_password) == 0)
                {
                    found = 1;
                    break;
                }
            }
            if (found)
            {
                fprintf(stdout, "\t[+] Password FOUND: %s\n", password);
            }
            else
            {
                fprintf(stdout, "\t[-] Password NOT FOUND\n");
            }
        }
        rewind(dictonary_fp);
    }

    fclose(password_fp);
    fclose(dictonary_fp);
}

void get_user_name_and_hashed_password(char *s, char *user, char *hashed_password)
{
    char *p = s;
    
    /* get user name */
    while (*p != ':')
    {
        *user++ = *p++;
    }
    *user = '\0';
    p++;

    /* get user's hashed password */
    while (*p != ':')
    {
        *hashed_password++ = *p++;
    }
    *hashed_password = '\0';

    return;
}

static inline void usage(char *prog)
{
    fprintf(stdout, "Usage: %s -f <password> -d <dictonary>\n", prog);
    return;
}