"use client";

import { motion } from "framer-motion";
import React from "react";
import { AuroraBackground } from "@/components/ui/aurora-background";
import { LoginForm } from "@/components/login-form"

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion"

export default function Home() {
  return (
    <>
      <AuroraBackground>
        <motion.div
          initial={{ opacity: 0.0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{
            delay: 0.3,
            duration: 0.8,
            ease: "easeInOut",
          }}
          className="relative flex flex-col gap-4 items-center justify-center px-4"
        >
          <div className="text-3xl md:text-7xl font-bold dark:text-white text-center">
            Introducing CGMPlus
          </div>
          <div className="font-extralight text-base md:text-4xl dark:text-neutral-200 py-1">
            supported by artificial intelligence
          </div>
          <button className="bg-black dark:bg-white rounded-full w-fit text-white dark:text-black px-5 py-2 m-5 font-bold">
            <a className="decoration-n white" href="#login">Try now</a>
          </button>
        </motion.div>
      </AuroraBackground>
      <motion.div
        initial={{ opacity: 0.0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{
          delay: 0.3,
          duration: 0.8,
          ease: "easeInOut",
        }}
        className="relative flex flex-col gap-4 items-center justify-center px-4"
      >
        <div id="login" className="flex min-h-svh flex-col items-center justify-center gap-6 bg-background p-6 md:p-10">
          <div className="w-full max-w-sm">
            <LoginForm />
          </div>
        </div>
      </motion.div>
    </>
  );
}