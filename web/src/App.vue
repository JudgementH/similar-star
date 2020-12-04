<template>
    <v-app app>
        <Bar/>
        <v-main><!-- 为应用程序提供正确的插槽 -->
            <v-container fluid><!-- 如果使用vue-router -->
                <router-view></router-view>
            </v-container>
        </v-main>
    </v-app>
</template>

<script>
    import Bar from "./components/Bar";

    export default {
        name: 'App',

        components: {
            Bar,
        },

        data: () => ({
            //
        }),
    };
</script>
