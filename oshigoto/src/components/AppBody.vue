<script setup lang="ts">
import JobDescription from './JobDescription.vue'
import JobPoint from './JobPoint.vue'
import { ref } from 'vue';

const role = ref("")
const location = ref("")
const nodeFlair = ref([])
const linkedIn = ref([])
const glints = ref([])
const internSg = ref([])
const google = ref([])
const points = ref([])

const onSearchBtnClick = () => {
    console.log(`role: ${role.value}`)
    console.log(`location: ${location.value}`)
}
</script>

<template>
    <div class="container">
        <!-- Settings form -->
        <div class="row my-3">
            <div class="col">
                <input 
                    type="text"
                    class="form-control"
                    placeholder="Role"
                    v-model="role"
                />
            </div>
            <div class="col">
                <input
                    type="text"
                    class="form-control"
                    placeholder="Location"
                    v-model="location"
                />
            </div>
            <div class="col-1">
                <button class="btn btn-primary" @click="onSearchBtnClick">
                    Search
                </button>
            </div>
        </div>

        <!-- 1st row -->
        <div class="row" >
            <div class="col">
                <div class = 'text-center'>
                    <h5>NodeFlair</h5>
                </div>
                <div class="list-group border overflow-auto" style="height:400px">
                    <JobDescription v-for="data in nodeFlair" :data="data"/>
                </div>
            </div>
            <div class="col">
                <div class = 'text-center'>
                    <h5>Most Common Phrases</h5>
                </div>
                <div class="list-group border overflow-auto" style="height:400px">
                    <JobPoint v-for="data in points" :data="data" />
                </div>
            </div>
            <div class="col">
                <div class = 'text-center'>
                    <h5>LinkedIn</h5>
                </div>
                <div class="list-group border overflow-auto" style="height:400px">
                    <JobDescription v-for="data in linkedIn" :data="data"/>
                </div>
            </div>
        </div>

        <!-- 2nd row -->
        <div class="row my-3">
            <div class="col">
                <div class = 'text-center'>
                    <h5>Glints</h5>
                </div>
                <div class="list-group border overflow-auto" style="height:400px">
                    <JobDescription v-for="data in glints" :data="data"/>
                </div>
            </div>
            <div class="col">
                <div class = 'text-center'>
                    <h5>InternSg</h5>
                </div>
                <div class="list-group border overflow-auto" style="height:400px">
                    <JobDescription v-for="data in internSg" :data="data"/>
                </div>
            </div>
            <div class="col">
                <div class = 'text-center'>
                    <h5>Google</h5>
                </div>
                <div class="list-group border overflow-auto" style="height:400px">
                    <JobDescription v-for="data in google" :data="data"/>
                </div>
            </div>
        </div>
    </div>
</template>