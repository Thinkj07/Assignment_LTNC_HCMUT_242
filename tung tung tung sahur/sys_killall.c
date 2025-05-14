/*
 * Copyright (C) 2025 pdnguyen of HCMC University of Technology VNU-HCM
 */

/* Sierra release
 * Source Code License Grant: The authors hereby grant to Licensee
 * personal permission to use and modify the Licensed Source Code
 * for the sole purpose of studying while attending the course CO2018.
 */

#include "common.h"
#include "syscall.h"
#include "stdio.h"
#include "libmem.h"
#include "queue.h"
#include <string.h>   // For strcmp
#include <stdlib.h> 

int __sys_killall(struct pcb_t *caller, struct sc_regs* regs)
{
    char proc_name[100];
    uint32_t data;

    uint32_t memrg = regs->a1;

    /* TODO: Get name of the target proc */
    //proc_name = libread..
    int i = 0;
    data = 0;
    while (data != -1 && i < 99) { // Set limitation for not overloading buffer
        libread(caller, memrg, i, &data);
        proc_name[i] = (char)data;
        if (data == -1 || data == 0) {
            proc_name[i] = '\0';
            break;
        }
        i++;
    }
    proc_name[i] = '\0';
    printf("The procname retrieved from memregionid %d is \"%s\"\n", memrg, proc_name);

    int prio;
    struct queue_t *queue;

    for (prio = 0; prio < MAX_PRIO; prio++) {
        queue = &caller->mlq_ready_queue[prio];
        if (caller->mlq_ready_queue == NULL) {
        printf("caller->mlq_ready_queue is NULL!\n");
        return -1;
    }
        if (empty(queue)) continue;

        int j;
        for (j = 0; j < queue->size; ) {
            struct pcb_t *proc = queue->proc[j];
            if (proc == NULL) {
            j++;
            continue;
        }
            if (strcmp(proc->path, proc_name) == 0 && proc != caller) {
                for (int k = j; k < queue->size - 1; k++) {
                    queue->proc[k] = queue->proc[k + 1];
                }
                queue->proc[queue->size - 1] = NULL;
                queue->size--;

                printf("Terminated process PID %d with name \"%s\"\n", proc->pid, proc->path);

                free(proc->code);
#ifdef MM_PAGING
                if (proc->mm) free(proc->mm);
#endif
            } else {
                j++;
            }
        }
    }

    queue = caller->running_list;
    if (!empty(queue)) {
        for (int j = 0; j < queue->size; ) {
            struct pcb_t *proc = queue->proc[j];

            if (strcmp(proc->path, proc_name) == 0 && proc != caller) {
                for (int k = j; k < queue->size - 1; k++) {
                    queue->proc[k] = queue->proc[k + 1];
                }
                queue->proc[queue->size - 1] = NULL;
                queue->size--;

                printf("Terminated process PID %d with name \"%s\" from running list\n", proc->pid, proc->path);

                free(proc->code);
#ifdef MM_PAGING
                if (proc->mm) free(proc->mm);
#endif
            } else {
                j++;
            }
        }
    }

    return 0;
}