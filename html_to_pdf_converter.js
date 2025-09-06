#!/usr/bin/env node

import puppeteer from 'puppeteer';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function convertHTMLtoPDF(htmlPath, outputPath) {
    try {
        // Check if HTML file exists
        if (!fs.existsSync(htmlPath)) {
            console.error('HTML file not found:', htmlPath);
            process.exit(1);
        }

        console.log('Starting PDF conversion...');
        
        // Launch browser (use system Chrome if PUPPETEER_EXECUTABLE_PATH is set)
        const browser = await puppeteer.launch({
            headless: 'new',
            args: ['--no-sandbox', '--disable-setuid-sandbox'],
            executablePath: process.env.PUPPETEER_EXECUTABLE_PATH || undefined
        });
        
        const page = await browser.newPage();
        
        // Navigate to the HTML file
        const fileUrl = 'file://' + path.resolve(htmlPath);
        console.log('Loading HTML from:', fileUrl);
        await page.goto(fileUrl, { waitUntil: 'networkidle0' });
        
        // Generate PDF
        console.log('Generating PDF...');
        await page.pdf({
            path: outputPath,
            format: 'A4',
            printBackground: true,
            margin: {
                top: '20mm',
                right: '15mm',
                bottom: '20mm',
                left: '15mm'
            }
        });
        
        await browser.close();
        console.log('✅ PDF created successfully:', outputPath);
        
    } catch (error) {
        console.error('Error converting HTML to PDF:', error);
        process.exit(1);
    }
}

// Parse command line arguments
const args = process.argv.slice(2);
if (args.length < 1) {
    console.log('Usage: node html_to_pdf_converter.js <input.html> [output.pdf]');
    console.log('If output.pdf is not specified, it will use the same name as input with .pdf extension');
    process.exit(1);
}

const inputFile = args[0];
const outputFile = args[1] || inputFile.replace(/\.html?$/i, '.pdf');

// Run conversion
convertHTMLtoPDF(inputFile, outputFile);