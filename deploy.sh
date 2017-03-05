#!/bin/bash

# adopted from https://github.com/timwis/static-api
set -ev && \
cd ./dist && \
mkdir gh-pages && \
cd ./gh-pages && \
remote_repo="https://${GITHUB_TOKEN}@github.com/${TRAVIS_REPO_SLUG}.git" && \
remote_branch="gh-pages" && \
git clone -b $remote_branch $remote_repo && \
git config user.name "Travis CI" && \
git config user.email "travis@srehwald.github.io" && \
cp -R ../dist/ ./ && \
git add . && \
git commit -m'build' && \
git push --quiet origin $remote_branch > /dev/null 2>&1 && \
rm -fr .git